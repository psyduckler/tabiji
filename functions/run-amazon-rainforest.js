const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771698979560_q1hdud",
  email: "psyduckler@gmail.com",
  destination: "Amazon Rainforest",
  start_date: "2026-02-28",
  end_date: "2026-03-04",
  group_size: "2",
  travel_style: "",
  dining: "",
  budget: "",
  requests: "",
  amount: "0.00",
  timestamp: "2026-02-21T18:36:19.560Z",
  status: "pending"
};

const itineraryData = {
  destination: "Amazon Rainforest, Brazil",
  countryEmoji: "🇧🇷",
  title: "Amazon Rainforest in 5 Days: Into the Wild Heart of the World",
  subtitle: "Manaus → Rio Negro → Jungle Lodge → Canopy Walks → River Communities",
  description: "A couple's expedition into the Amazon — the largest tropical rainforest on Earth, where rivers run black and white, pink dolphins surface at sunset, and the jungle hums with life 24 hours a day. Late February is wet season: the rivers are high, the forest floods, and you'll canoe through the treetops. It's raw, beautiful, and unlike anywhere else on the planet.",
  duration: "4 nights / 5 days",
  dates: "Feb 28 – Mar 4, 2026",
  budget: "Moderate",
  pace: "Adventure — jungle treks, boat excursions, wildlife spotting",
  bestFor: "Couples, nature lovers & adventure seekers",
  highlights: [
    "Meeting of the Waters — where the Rio Negro and Solimões collide without mixing",
    "Pink river dolphins (botos) surfacing at sunset",
    "Canopy walkway — suspended bridges 30 meters above the jungle floor",
    "Flooded forest canoe trips through submerged trees",
    "Caiman spotting on nighttime boat expeditions",
    "Piranha fishing on blackwater tributaries",
    "Visiting ribeirinho river communities",
    "Sunrise over the jungle canopy — howler monkeys as your alarm clock",
    "Manaus Opera House — Belle Époque grandeur in the middle of the jungle",
    "Amazonian cuisine — tucunaré, tacacá, açaí fresh from the tree"
  ],
  essentials: [
    { title: "🛫 Getting There", text: "Fly into Manaus (MAO) — Brazil's gateway to the Amazon. Direct flights from São Paulo (4h) and Brasília (3.5h). Most jungle lodges arrange transfers from Manaus: typically a 1-3 hour boat ride upriver. Book lodge transfers in advance — you can't just show up at the jungle." },
    { title: "💵 Budget Tips", text: "Jungle lodges are all-inclusive: expect $150-300/night pp including meals, guides, and excursions. Manaus city meals are $8-15 for street food, $25-40 for sit-down restaurants. Budget $20-30 for Manaus taxis/Uber around the city. Tips for guides: $10-20/day is appreciated and customary." },
    { title: "🌧️ Wet Season (Feb-Mar)", text: "This is peak wet season — rivers are at their highest, and the várzea (floodplain forest) is submerged up to 10 meters. This is actually the BEST time for canoe trips through the flooded forest canopy. Expect daily rain (usually afternoon downpours, 1-2 hours), 85-95°F (29-35°C), and extreme humidity. Mornings are often clear and stunning." },
    { title: "🧴 What to Pack", text: "Long sleeves and pants (mosquito protection), waterproof bag for electronics, reef-safe sunscreen, strong DEET insect repellent, waterproof hiking boots or sandals, rain jacket, headlamp for night excursions. Leave the fancy clothes — you will get wet, muddy, and sweaty. That's the point." },
    { title: "💉 Health & Safety", text: "Yellow fever vaccination required (bring your certificate). Malaria prophylaxis recommended — consult your travel doctor 4-6 weeks before. Drink only bottled/filtered water. The jungle is surprisingly safe with a guide — jaguars, snakes, and spiders avoid humans. Mosquitoes are the real challenge: cover up at dawn and dusk." },
    { title: "📱 Connectivity", text: "Expect limited to zero cell service at jungle lodges. Wi-Fi may exist at the main lodge but will be slow and unreliable. Embrace the disconnect — it's part of the experience. Download offline maps of Manaus before you go. WhatsApp works when you have signal." }
  ],
  days: [
    {
      num: 1,
      title: "Manaus: Gateway to the Amazon",
      neighborhoods: "Centro Histórico · Mercado Municipal · Porto de Manaus",
      date: "Feb 28",
      mapPins: [
        { lat: -3.1303, lng: -60.0233, label: "Teatro Amazonas", num: 1, cat: "activity", desc: "Stunning 1896 opera house — rubber boom opulence" },
        { lat: -3.1340, lng: -60.0248, label: "Mercado Municipal Adolpho Lisboa", num: 2, cat: "food", desc: "Historic market with Amazonian fish and fruits" },
        { lat: -3.1375, lng: -60.0270, label: "Porto de Manaus", num: 3, cat: "activity", desc: "Floating port on the Rio Negro" },
        { lat: -3.1285, lng: -60.0215, label: "Largo de São Sebastião", num: 4, cat: "activity", desc: "Beautiful plaza surrounding the opera house" },
        { lat: -3.1320, lng: -60.0260, label: "Palácio Rio Negro", num: 5, cat: "activity", desc: "Former rubber baron mansion, now a cultural center" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Teatro Amazonas", description: "Start at the Teatro Amazonas — a jaw-dropping 1896 opera house built during the rubber boom, when Manaus was one of the richest cities on Earth. Italian marble, French ironwork, English furniture, and a dome painted with four continents. It's surreal: a European opera house dropped into the middle of the Amazon jungle. The 30-minute guided tour is excellent and cheap.", details: ["📍 Largo de São Sebastião · R$20 (~$4) for guided tour · Open Mon-Sat 9am-5pm", "💡 The plaza outside (Largo de São Sebastião) has a distinctive wave pattern in the cobblestones representing the Meeting of the Waters. Grab coffee at one of the cafés and just take it in."] },
            { title: "Centro Histórico Walk", description: "Explore Manaus's faded colonial center. The city boomed spectacularly during the rubber era (1880-1912) and the grand buildings remain — peeling, tropical, and atmospheric. Visit the Palácio Rio Negro (rubber baron mansion turned cultural center) and walk along the waterfront. Manaus is gritty, chaotic, and fascinating.", details: ["💡 Manaus is hot and humid — pace yourself. Walk in the morning, rest during the midday heat, and carry water everywhere."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Hotel or Café near Largo de São Sebastião", description: "Start with strong Amazonian coffee and tapioca crepes (beiju) — made from cassava flour, filled with cheese, coconut, or banana. Simple, local, and perfect in the morning heat. The cafés around the opera house plaza are pleasant and shaded.", meta: "$5-10pp · Walk-in · Try the tucumã (Amazonian palm fruit) tapioca" }
          ],
          tips: [{ type: "tip", text: "Manaus is a city of 2 million people — it's not a small jungle town. It has Ubers, malls, and traffic. But the Amazon starts literally at the city limits. The contrast is part of the magic." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Mercado Municipal Adolpho Lisboa", description: "Dive into the Mercado Municipal — Manaus's historic market modeled after Les Halles in Paris. The fish section is mind-blowing: enormous pirarucu (the world's largest freshwater fish, up to 3 meters), tucunaré, tambaqui, and species you've never seen. The fruit section has açaí, cupuaçu, bacaba, and dozens of Amazonian fruits that don't exist outside the region. It's sensory overload in the best way.", details: ["📍 Rua dos Barés, 46 · Open Mon-Sat 6am-6pm, Sun 6am-1pm · Free entry", "💡 Try a bowl of tacacá from one of the market vendors — a traditional Amazonian soup made with jambu (a numbing herb), dried shrimp, and tucupi (fermented cassava juice). It's unlike anything you've ever tasted."] },
            { title: "Porto de Manaus & Waterfront", description: "Walk to the Porto de Manaus — the floating port that rises and falls up to 15 meters with the river's annual flood cycle. In late February, the water is rising fast. Watch the river traffic: cargo boats stacked impossibly high, ferries heading to river communities, and fishermen returning with their catch. The scale of the Rio Negro here is oceanic.", details: ["💡 The Ponte sobre o Rio Negro (Rio Negro Bridge) is visible from the port — a 3.6 km bridge that was impossible to build until 2011."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Tambaqui de Banda", description: "The best Amazonian fish restaurant in Manaus. The signature dish is tambaqui de banda — a massive freshwater fish slow-roasted over charcoal and served with farofa, vinaigrette, and rice. The costela de tambaqui (fish ribs — yes, freshwater fish ribs) are extraordinary. Rustic, delicious, and genuinely local.", meta: "$15-25pp · Av. Boulevard Álvaro Maia · Reservations for dinner, walk-in for lunch" }
          ],
          tips: [{ type: "reddit", text: "Tambaqui de Banda is the one restaurant in Manaus that everyone agrees on. The fish is insane — Amazon river fish just hits different. Get the tambaqui ribs and the tacacá.", cite: "r/travel" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Transfer to Jungle Lodge", description: "Late afternoon, meet your lodge transfer at the port or hotel. The boat ride to your jungle lodge (1-3 hours depending on location) is your first real Amazon experience: the city fades away, the river widens, and the jungle closes in. Watch for dolphins, herons, and the sunset turning the Rio Negro into liquid gold. By the time you arrive, you're in another world.", details: ["💡 Recommended lodges: Juma Amazon Lodge (stilts over the lake, excellent guides), Anavilhanas Lodge (Rio Negro, upscale), or Amazon Tupana Lodge (budget-friendly, authentic). Book directly for best rates."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Lodge Dinner", description: "Your first jungle dinner — lodges serve Amazonian cuisine: grilled tucunaré (peacock bass), river prawn stew, roasted plantains, fresh açaí, and tropical fruit juices. Dining is communal, and your guide will brief you on tomorrow's adventures. Eat well — jungle days start early.", meta: "Included with lodge · Communal dining · Expect Amazonian fish, tropical fruits, cassava dishes" }
          ],
          tips: [{ type: "tip", text: "The night sounds of the Amazon are extraordinary — frogs, insects, birds, and howler monkeys create a symphony that never stops. Step outside your cabin after dinner, turn off your headlamp, and just listen. Your eyes will adjust and you might see fireflies or bioluminescent fungi." }]
        }
      ]
    },
    {
      num: 2,
      title: "Meeting of the Waters & Flooded Forest",
      neighborhoods: "Rio Negro · Rio Solimões · Várzea Forest",
      date: "Mar 1",
      mapPins: [
        { lat: -3.1300, lng: -59.8900, label: "Meeting of the Waters", num: 1, cat: "activity", desc: "Two rivers collide without mixing for 6 km" },
        { lat: -3.2500, lng: -60.1500, label: "Flooded Forest", num: 2, cat: "activity", desc: "Canoe through submerged canopy" },
        { lat: -3.1800, lng: -60.0800, label: "Lago do Janauari", num: 3, cat: "activity", desc: "Ecological park with giant water lilies" },
        { lat: -3.2000, lng: -60.1200, label: "Dolphin Spotting Area", num: 4, cat: "activity", desc: "Pink and grey river dolphins" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Meeting of the Waters", description: "The day's first stop is one of nature's most surreal spectacles: the Encontro das Águas, where the black Rio Negro and the sandy-brown Rio Solimões flow side by side for 6 kilometers without mixing. The difference in temperature, speed, and density keeps them separate. You'll boat right into the confluence — one side of the boat in black water, the other in brown. It looks photoshopped. It's real.", details: ["📍 About 10 km east of Manaus, accessible by boat", "💡 The color contrast is most dramatic on sunny mornings — the black water looks like tea and the brown water looks like café au lait. Try dipping your hands in both sides — the temperature difference is noticeable."] },
            { title: "Lago do Janauari & Giant Water Lilies", description: "Visit the Janauari Ecological Park to see the Victoria amazonica — giant water lilies with pads up to 3 meters across. They're strong enough to support a small child. In wet season (right now), the lilies are at their peak. Your guide will also point out caimans, monkeys, and sloths in the surrounding trees.", details: ["📍 Accessible by boat from Manaus or en route from Meeting of the Waters", "💡 The lilies bloom at night — the white flowers are pollinated by beetles attracted to their heat and scent. By morning, the flowers turn pink."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Lodge Breakfast", description: "Wake with the jungle at 5:30-6am. Breakfast at the lodge: fresh tropical fruits (papaya, mango, passion fruit, watermelon), tapioca pancakes, strong Brazilian coffee, and fresh juices. Eat on the deck overlooking the river — howler monkeys providing the soundtrack.", meta: "Included · 6:00-7:30am typically · Early fuel for a big day" }
          ],
          tips: [{ type: "tip", text: "Apply insect repellent before breakfast and reapply after every swim or heavy sweat. Dawn and dusk are peak mosquito hours. Long sleeves + DEET is the jungle uniform." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Flooded Forest Canoe Trip", description: "This is the Amazon experience you came for. In wet season, the várzea forest floods up to 10 meters — you literally canoe through the treetops. Your guide paddles silently through submerged trees, pointing out sloths, monkeys, toucans, poison dart frogs, and the occasional anaconda draped over a branch. The water is mirror-still and the canopy filters the light into green cathedral beams. It's profound silence broken only by bird calls and dripping water.", details: ["💡 Bring a waterproof bag/case for your phone and camera — you WILL get splashed. A GoPro or waterproof camera is ideal.", "💡 Stay still in the canoe and whisper — the more silent you are, the more wildlife appears. Your guide has eagle eyes for camouflaged animals."] },
            { title: "Dolphin Watching", description: "On the boat ride back, watch for botos — Amazon pink river dolphins. These prehistoric-looking creatures are genuinely pink (especially the males) and surface regularly in the late afternoon. Grey dolphins (tucuxi) are also common. Your guide will know their favorite spots. Seeing a pink dolphin surface in golden late-afternoon light is one of those moments that rewires your brain.", details: ["💡 Pink dolphins are curious and often approach boats. The males are pinker — it's a combination of blood vessels near the skin surface and scarring from fighting. They're more active in late afternoon."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Riverside Picnic or Lodge Lunch", description: "Some lodges pack a riverside picnic — grilled fish wrapped in banana leaves, farinha (toasted cassava flour), fresh fruit, and river-cooled drinks. Eating freshly caught fish on the riverbank while macaws fly overhead is peak Amazon.", meta: "Included · Your guide may catch and grill fish on the spot" }
          ],
          tips: [{ type: "reddit", text: "The flooded forest canoe trip during wet season is genuinely one of the most magical things I've ever done. Paddling through the canopy in complete silence, watching a sloth move in slow motion 3 feet from your face. Nothing prepares you for it.", cite: "r/travel" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Caiman Spotting Night Expedition", description: "After dinner, head out on a night boat expedition for caiman (Amazonian alligators). Your guide uses a flashlight to spot the red eye-shine of caimans along the riverbank. You'll get close — really close. The guide may even catch a small one for you to hold and photograph before releasing it. The jungle at night is a completely different world: louder, darker, and electric with life.", details: ["📍 Departs from lodge after dinner, typically 8-9pm, 1-2 hours", "💡 Bring your headlamp and insect repellent. Wear long sleeves. The night boat ride under the stars is incredible — zero light pollution, the Milky Way stretches from horizon to horizon."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Lodge Dinner", description: "Tonight's lodge dinner might feature pirarucu — the Amazon's legendary giant fish (up to 3 meters). Served grilled with lime and herbs, the meat is firm and clean-tasting. Paired with river prawn farofa, grilled plantains, and a caipirinha made with Amazonian fruits (cupuaçu or caju). The dining table conversations with fellow travelers are always fascinating.", meta: "Included · Communal dining · Try the pirarucu if it's on the menu" }
          ],
          tips: [{ type: "tip", text: "The Southern Hemisphere stars are different — look for the Southern Cross (Crux) and the Magellanic Clouds. Your guide may know the indigenous constellations, which are completely different from Western ones." }]
        }
      ]
    },
    {
      num: 3,
      title: "Jungle Trek, Canopy Walk & Piranha Fishing",
      neighborhoods: "Primary Forest · Canopy Tower · Blackwater Tributaries",
      date: "Mar 2",
      mapPins: [
        { lat: -3.2800, lng: -60.1800, label: "Jungle Trek", num: 1, cat: "activity", desc: "Guided hike through primary rainforest" },
        { lat: -3.2700, lng: -60.1700, label: "Canopy Walkway", num: 2, cat: "activity", desc: "Suspended bridges 30m above the forest floor" },
        { lat: -3.3000, lng: -60.2000, label: "Piranha Fishing", num: 3, cat: "activity", desc: "Catch (and eat) red-bellied piranha" },
        { lat: -3.2600, lng: -60.1600, label: "Medicinal Plants Trail", num: 4, cat: "activity", desc: "Traditional Amazonian plant knowledge" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Primary Jungle Trek", description: "Your guide leads you into primary (old-growth) rainforest. This is the real deal: massive trees with buttress roots taller than you, lianas thick as your arm, and a canopy so dense that the forest floor is in perpetual twilight. Your guide will show you survival techniques — which vines hold drinkable water, which bark treats malaria, which ants you can eat (lemon ants — they taste like citrus). You'll learn to read the forest: animal tracks, territorial markings, medicinal plants.", details: ["💡 Wear long pants, waterproof boots, and tuck pants into socks (tick prevention). Bring water and snacks.", "💡 The jungle floor is surprisingly dark — the canopy absorbs 95% of sunlight. Your eyes adjust, and the details emerge: tiny frogs, massive spiders, columns of leaf-cutter ants carrying their green cargo."] },
            { title: "Canopy Walkway", description: "Climb to the canopy walkway — a series of suspended rope bridges 25-35 meters above the forest floor. Up here, the world transforms: you're at eye level with toucans, macaws, and howler monkeys. The perspective shift is staggering — the forest below looks like a green ocean, and the sky opens up above. On a clear morning, you can see for miles over unbroken canopy.", details: ["📍 Available at several lodges (Juma, INPA reserves) · Some have observation towers up to 40m", "💡 Go early morning (6-7am) for the best birdwatching. Bring binoculars. The canopy is where 90% of Amazon biodiversity lives — this is the real jungle, not the floor."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Pre-Dawn Lodge Breakfast", description: "Early breakfast (5:30am) before the trek. The jungle is most active at dawn — don't sleep in. Strong coffee, fruit, granola, and tapioca to fuel the morning. Watch the mist rise off the river as the sun burns through.", meta: "Included · 5:30-6:30am · Early start for the best wildlife" }
          ],
          tips: [{ type: "reddit", text: "Do the canopy walk at sunrise if your lodge offers it. The birdlife up there in the early morning is absolutely unreal. I saw 4 species of toucan and a troop of squirrel monkeys in 30 minutes. Worth every early alarm.", cite: "r/travel" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Piranha Fishing", description: "Time for one of the Amazon's most iconic activities: piranha fishing. Using a simple stick, line, and raw meat as bait, you'll fish in blackwater tributaries. Red-bellied piranhas are aggressive and plentiful — you'll feel them strike. Your guide will handle the hooks (piranha teeth are no joke). Whatever you catch gets grilled for a snack. They're small, bony, but surprisingly tasty.", details: ["💡 Piranha fishing works best in calm, shady backwaters. The fish are attracted by splashing — your guide may slap the water to draw them in.", "💡 Despite their reputation, piranhas almost never attack humans. They're scavengers, not predators. You can swim in the same water (but maybe not with an open wound)."] },
            { title: "River Community Visit", description: "Visit a ribeirinho community — families who live along the river in stilt houses, fishing and farming as they have for generations. Your guide will introduce you to a local family. You might see how they process cassava (the Amazon staple), harvest açaí, or weave baskets. These communities are the living culture of the Amazon — warm, generous, and endlessly resourceful.", details: ["💡 Bring small gifts if you'd like — school supplies (notebooks, pens) are always appreciated. Ask your guide what's appropriate.", "💡 The ribeirinhos have deep ecological knowledge passed down through generations. Their understanding of the river's moods, the forest's rhythms, and animal behavior is extraordinary."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Freshly Caught Piranha & River Fare", description: "Your piranhas, fried crispy over a wood fire on the riverbank. They're bony but the flesh is sweet and firm. Accompanied by farinha, fresh lime, and river-cooled drinks. Eating what you caught, where you caught it, surrounded by jungle — this is the Amazon experience distilled.", meta: "Included · Caught & cooked on the spot" }
          ],
          tips: [{ type: "tip", text: "Swimming in the Amazon is safe in most areas your guide selects — the black water rivers (Rio Negro tributaries) have fewer mosquitoes because the tannin-rich water is inhospitable to larvae. Ask your guide before jumping in." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Sunset from the Lodge Deck", description: "Watch the sunset from the lodge deck — the Amazon sunset is a slow, epic event. The sky turns orange, pink, and purple over the endless canopy. Dolphins surface in the golden water. Parrots fly home in pairs. The transition from day to night in the Amazon is dramatic: the bird sounds fade and the frog-insect orchestra tunes up. Enjoy a caipirinha and reflect on the wildest place you've ever been.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Lodge Farewell Dinner", description: "A special dinner tonight: your lodge might serve jaraqui assado (roasted river fish), caldeirada amazônica (fish stew), or tucunaré na brasa (charcoal-grilled peacock bass). Fresh açaí for dessert — not the frozen stuff from home, but thick, purple, and slightly savory. This is Amazonian cuisine at its purest.", meta: "Included · Communal dining · Ask about any regional specialties" }
          ],
          tips: [{ type: "reddit", text: "Real Amazonian açaí is NOTHING like what you get at smoothie shops. It's thick, slightly bitter, earthy, and usually eaten with fish and farinha. The sweetened tourist version is fine, but try the real way at least once.", cite: "r/travel" }]
        }
      ]
    },
    {
      num: 4,
      title: "Sunrise Expedition, Indigenous Culture & River Life",
      neighborhoods: "Upstream tributaries · Indigenous community · Lake systems",
      date: "Mar 3",
      mapPins: [
        { lat: -3.2200, lng: -60.1400, label: "Sunrise Boat Trip", num: 1, cat: "activity", desc: "Dawn on the river — peak birdwatching" },
        { lat: -3.3200, lng: -60.2200, label: "Indigenous Community", num: 2, cat: "activity", desc: "Cultural exchange and traditional crafts" },
        { lat: -3.2800, lng: -60.1900, label: "Lake Expedition", num: 3, cat: "activity", desc: "Searching for giant otters and hoatzins" },
        { lat: -3.2500, lng: -60.1600, label: "Swimming Spot", num: 4, cat: "activity", desc: "Swim in tannin-rich black water" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Sunrise Boat Expedition", description: "Leave the lodge at 5am for a sunrise boat trip. The pre-dawn jungle is cool and misty. As the sun breaks, the forest ignites: macaws streak across the orange sky, herons stalk the shallows, and kingfishers dive. Your guide will navigate narrow igarapés (forest streams) looking for wildlife. Early morning is prime time for sloths, monkeys, and the elusive hoatzin (a prehistoric-looking bird).", details: ["💡 Binoculars are essential for the sunrise trip. A telephoto lens if you have one. The light at dawn is golden and soft — photographer's dream.", "💡 The hoatzin (stinkbird) looks like a punk rock dinosaur — mohawk crest, red eyes, blue face. They're clumsy flyers and smell terrible. Utterly unforgettable."] },
            { title: "Giant Otter Search", description: "Navigate to a lake system to search for giant otters — the Amazon's apex aquatic predator. These 6-foot-long otters live in family groups and are incredibly vocal and playful. Finding them is not guaranteed, but when you do, it's breathtaking: they pop up, chatter at each other, crunch fish, and dive in synchronized patterns. They're one of the Amazon's most charismatic species.", details: ["💡 Giant otters are endangered — there are only about 5,000 left. Seeing them in the wild is a privilege. Keep quiet and maintain distance; they're curious but territorial."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Post-Expedition Lodge Breakfast", description: "Return to the lodge hungry at 8-9am. A full breakfast spread: scrambled eggs, fresh bread, tropical fruits, cheese, ham, and multiple juice options (passion fruit, cashew, guava). The lodge chef may make you a custom tapioca. You've earned it.", meta: "Included · 8:00-9:30am after morning excursion" }
          ],
          tips: [{ type: "tip", text: "The early morning and late afternoon boat trips are the highlights of any Amazon trip. Don't skip them for sleep. You can nap in a hammock during the midday heat — that's what the hammock is for." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Indigenous Community Visit", description: "Visit an indigenous community — many lodges partner with local communities for cultural exchanges. You might see traditional dances, try your hand at blow-dart hunting, learn about ancestral forest knowledge, or buy handmade crafts directly from artisans. These visits are done respectfully and provide income to the community. It's a window into a worldview centered on the river and the forest.", details: ["💡 Photography rules vary by community — always ask first. Some communities prefer no photos of children.", "💡 Handmade crafts (woven baskets, seed jewelry, blow darts) make meaningful souvenirs and directly support the community."] },
            { title: "Black Water Swimming", description: "Cool off with a swim in the Rio Negro's tannin-rich black water. The water is naturally acidic and tea-colored (from decomposing leaves) — which means fewer mosquitoes and a surprisingly soft feel on your skin. It's safe, warm (80°F+), and the most refreshing thing in the jungle. Jump off the boat, float on your back, and stare up at the canopy. Life-changing.", details: ["💡 The black water is called 'the Amazon's natural swimming pool' because the acidity keeps bacteria and mosquito larvae low. It's genuinely clean and safe."] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Lodge Lunch", description: "Grilled river fish, rice, beans, farofa, and salad. Simple, satisfying, and perfectly suited to the heat. Try the cupuaçu juice — it's a cousin of cacao with a unique tangy-tropical flavor. Or a cold Guaraná Antarctica (Brazil's favorite soda).", meta: "Included · Midday meal at the lodge" }
          ],
          tips: [{ type: "reddit", text: "Swimming in the Rio Negro is one of those things that sounds sketchy but is genuinely safe and amazing. The water is warm, clean (naturally filtered by tannins), and there are no mosquitoes. I swam there for 3 days and it was the highlight of my Amazon trip.", cite: "r/solotravel" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Last Night in the Jungle", description: "Your last evening in the Amazon. After dinner, sit on the lodge deck and take it all in. The symphony of frogs and insects, the occasional splash of a dolphin or caiman, the Southern Cross hanging over the canopy. Your guide might share stories about the forest — legends of the Curupira (forest protector), the Boto (dolphin shapeshifter), and the Mapinguari (Amazon sasquatch). The Amazon's mythology is as rich as its biodiversity.", details: ["💡 Ask your guide about the legend of the Boto — the pink dolphin that transforms into a handsome man at night to seduce women at river parties. It's Brazil's most famous folk tale."] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Special Lodge Dinner", description: "Your final jungle dinner. The lodge may prepare a special regional dish: pato no tucupi (duck in fermented cassava sauce — a Pará classic), or moqueca amazônica (fish stew with coconut milk and dendê oil). Exchange contacts with fellow travelers and tip your guide generously — they showed you their home.", meta: "Included · Communal farewell dinner" }
          ],
          tips: [{ type: "tip", text: "Tip your guide $10-20/day total for the stay. They work incredibly hard, know the forest intimately, and their income depends on tourism. If your guide was exceptional, leave a review on TripAdvisor — it directly impacts their livelihood." }]
        }
      ]
    },
    {
      num: 5,
      title: "Departure: From Jungle to City",
      neighborhoods: "Lodge · Rio Negro · Manaus",
      date: "Mar 4",
      mapPins: [
        { lat: -3.2500, lng: -60.1500, label: "Lodge Departure", num: 1, cat: "activity", desc: "Last morning in the jungle" },
        { lat: -3.1300, lng: -60.0233, label: "Manaus", num: 2, cat: "activity", desc: "Return to civilization" },
        { lat: -3.0386, lng: -60.0498, label: "Aeroporto Eduardo Gomes", num: 3, cat: "activity", desc: "Manaus International Airport (MAO)" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Final Sunrise & Lodge Departure", description: "One last jungle sunrise. If you're up for it, take a solo walk on the lodge's trail — the forest is different when you're alone with it. Then pack up, say goodbye to the lodge staff (they'll remember you), and board the boat back to Manaus. The return boat ride is bittersweet — the jungle gradually gives way to scattered houses, then suburbs, then the city skyline. You'll re-enter civilization with different eyes.", details: ["💡 The return boat ride is 1-3 hours. Bring a book or just watch the river. You might see dolphins one last time on the way back."] },
            { title: "Last Stop in Manaus (if time allows)", description: "If your flight is in the afternoon, you have time for a final Manaus stop. Recommendations: the MUSA (Museu da Amazônia) botanical garden for a last jungle fix, the Praia da Ponta Negra waterfront for a river view, or a final meal at a Manaus restaurant. If you're heading straight to the airport, Eduardo Gomes International (MAO) is 15 minutes from downtown.", details: ["📍 MAO airport is close to downtown — even with traffic, 20-30 minutes max", "💡 Buy Amazonian souvenirs at the airport: guaraná powder (natural energy), Amazonian chocolate, tucumã oil, and artisanal cachaça."] }
          ],
          meals: [
            { type: "☕ Brunch", name: "Café Regional or Airport Meal", description: "A last Amazonian meal: tacacá (the numbing jambu soup), a final tapioca, or grilled tucunaré sandwich. If at the airport, the food options are decent — grab a pão de queijo (cheese bread) and a strong café. You're leaving the Amazon fuller than when you arrived — in every sense.", meta: "$8-15pp · Manaus or airport · Keep it simple" }
          ],
          tips: [{ type: "tip", text: "The Amazon changes you. You'll go home and notice how loud, bright, and artificial everything feels. That's normal. You just spent days in the world's most biodiverse ecosystem — a place that produces 20% of Earth's oxygen. You'll be back." }]
        }
      ]
    }
  ]
};

// Run fulfillment
(async () => {
  try {
    const result = fulfillOrder(order, itineraryData);
    console.log('✅ Fulfillment complete:', JSON.stringify(result, null, 2));
  } catch (err) {
    console.error('❌ Fulfillment failed:', err.message);
    process.exit(1);
  }
})();
