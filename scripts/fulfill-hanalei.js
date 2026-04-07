const fulfillOrder = require('./functions/fulfill-order');

const order = {
  id: 'order_1771304115175_gbo9ah',
  email: 'bernard.j.huang@gmail.com',
  destination: 'Hanalei, HI, USA',
  startDate: '2026-07-02',
  endDate: '2026-07-05',
  groupSize: 2,
  requests: 'romantic',
};

const itineraryData = {
  destination: "Hanalei, Kauai",
  countryEmoji: "🇺🇸",
  title: "Romance on Kauai's North Shore",
  subtitle: "3 days of sunsets, sea cliffs & island intimacy",
  description: "A romantic escape for two along Kauai's lush North Shore — from golden Hanalei Bay sunsets to the dramatic Na Pali Coast. Perfectly paced for couples who want adventure wrapped in tranquility.",
  duration: "3 days / 3 nights",
  dates: "Jul 2 – Jul 5, 2026",
  budget: "$$–$$$",
  pace: "Relaxed",
  bestFor: "Couples · Romance · Nature · Beach",

  essentials: [
    { title: "🚗 Getting Around", text: "Rent a car at Lihue Airport (OGG). The drive to Hanalei is ~40 min on the scenic Kuhio Highway. A car is essential — no rideshare coverage on the North Shore." },
    { title: "☀️ Weather", text: "July is peak dry season — expect 80–85°F, occasional brief tropical showers, and spectacular sunsets. North Shore gets more rain than the south, keeping everything impossibly green." },
    { title: "🏖️ Beach Gear", text: "Bring reef-safe sunscreen (required by Hawaii law), snorkel gear (or rent in Hanalei), and water shoes for rocky shoreline walks." },
    { title: "🍽️ Reservations", text: "Book Mediterraneo and Bar Acuda at least 2 weeks ahead — they're small and fill fast in summer. Food trucks are first-come, first-served." },
    { title: "📱 Connectivity", text: "Cell service is spotty past Princeville. Download offline maps. Embrace the disconnect — it's part of the magic." },
    { title: "🌺 Respect", text: "Stay on marked trails, don't stack rocks (they're often sacred), and never turn your back on the ocean. Hawaiian culture runs deep here — be a guest, not a tourist." },
  ],

  days: [
    {
      num: 1,
      neighborhoods: "Hanalei Bay · Hanalei Town · Waioli",
      title: "Arriving in Paradise",
      description: "Settle into the North Shore rhythm — toes in the sand, salt on your skin, sunset cocktails in hand.",
      timeBlocks: [
        {
          label: "Afternoon",
          activities: [
            {
              title: "Hanalei Bay Beach Walk",
              description: "After picking up your rental car and checking in, head straight to Hanalei Bay. This crescent of golden sand backed by emerald mountains is one of the most beautiful bays in the world. Wade in the gentle shorebreak, lay out on the sand, or walk the full 2-mile crescent hand-in-hand.",
              details: [
                "📍 Hanalei Beach Park — free parking at the pier or Black Pot Beach",
                "🕐 Arrive by 2–3 PM to soak in the afternoon light",
                "🌊 Summer swells are typically calm — safe for swimming"
              ]
            }
          ],
          tips: [
            { type: "tip", text: "The view from the Hanalei Valley Lookout on the drive in is jaw-dropping — pull over at the overlook just past Princeville for your first 'wow' moment." }
          ]
        },
        {
          label: "Evening",
          meals: [
            {
              type: "🍷 Dinner",
              name: "Mediterraneo",
              description: "Intimate Italian restaurant tucked in the Hanalei Colony Resort. Handmade pasta, fresh-caught fish, candlelit tables. The most romantic dinner on the North Shore.",
              meta: "$$$ · Reservations essential · 5-min drive west of Hanalei"
            }
          ],
          activities: [
            {
              title: "Sunset at Hanalei Pier",
              description: "Walk to the iconic Hanalei Pier for your first Kauai sunset. The sky turns sherbet-pink behind Bali Hai (Mt. Makana) — a scene so perfect it inspired the South Pacific movie. Bring a bottle of wine and two cups.",
              details: [
                "🌅 Sunset ~7:10 PM in July",
                "📸 Best photos from the east end of the pier looking west"
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 22.2095, lng: -159.5037, label: "Hanalei Valley Lookout", num: 1, cat: "attraction", desc: "Panoramic overlook of taro fields and mountains" },
        { lat: 22.2089, lng: -159.5070, label: "Hanalei Bay", num: 2, cat: "beach", desc: "Iconic crescent bay — swimming, sunbathing, beach walks" },
        { lat: 22.2097, lng: -159.5014, label: "Hanalei Pier", num: 3, cat: "attraction", desc: "Historic pier — best sunset spot in town" },
        { lat: 22.2284, lng: -159.5701, label: "Mediterraneo", num: 4, cat: "restaurant", desc: "Romantic Italian — handmade pasta & candlelit tables" }
      ]
    },
    {
      num: 2,
      neighborhoods: "Na Pali Coast · Hanalei · Princeville",
      title: "Na Pali & Fireworks on the Fourth",
      description: "The marquee day — a Na Pali Coast catamaran cruise followed by Fourth of July celebrations under the stars. July 4th on Kauai is laid-back and magical.",
      timeBlocks: [
        {
          label: "Morning",
          meals: [
            {
              type: "☕ Breakfast",
              name: "Hanalei Bread Company",
              description: "Beloved local bakery with fresh pastries, açaí bowls, and strong Kauai coffee. Grab a window seat and watch Hanalei wake up.",
              meta: "$ · Cash & card · Opens 7 AM"
            }
          ]
        },
        {
          label: "Mid-Morning → Afternoon",
          activities: [
            {
              title: "Na Pali Coast Catamaran Cruise",
              description: "The highlight of any Kauai trip. Board a catamaran from Port Allen or Hanalei (summer only) for a 4–5 hour cruise along the Na Pali Coast. Towering 3,000-ft sea cliffs, hidden waterfalls, spinner dolphins, and sea turtles. Many boats include snorkeling, lunch, and drinks. Book a morning departure for calmer seas.",
              details: [
                "🚤 Recommended: Captain Andy's or Holo Holo Charters",
                "⏰ Typical departure 7–8 AM, return by noon",
                "🐬 Dolphin & sea turtle sightings are nearly guaranteed in summer",
                "💡 Book well in advance — July 4th week sells out fast"
              ]
            }
          ],
          tips: [
            { type: "tip", text: "Take Dramamine 30 min before if you're prone to seasickness. The Na Pali swells can be moderate even in summer." }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Relax & Recharge",
              description: "After the cruise, take a couples nap or lounge by the pool. The afternoon heat is perfect for slowing down before the evening festivities.",
              details: []
            }
          ]
        },
        {
          label: "Evening — July 4th 🎆",
          meals: [
            {
              type: "🍽️ Dinner",
              name: "Bar Acuda",
              description: "Hanalei's best tapas bar — locally sourced small plates, excellent wine list, and a warm buzzy atmosphere. Perfect for sharing plates and stealing bites. Try the seared ahi and grilled local catch.",
              meta: "$$$ · Reservations strongly recommended · Hanalei Center"
            }
          ],
          activities: [
            {
              title: "Fourth of July in Hanalei",
              description: "Hanalei celebrates the 4th with a relaxed community vibe — expect live music at the bandstand, locals gathering on the beach, and fireworks over Hanalei Bay (typically launched from the pier area). Grab a spot on the sand with a blanket and watch the sky light up over the mountains.",
              details: [
                "🎆 Fireworks usually start around 8:30–9 PM",
                "🎶 Check Hanalei community boards for live music schedule",
                "🍺 Tahiti Nui bar often has a July 4th party — swing by for a mai tai"
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 22.2082, lng: -159.5043, label: "Hanalei Bread Company", num: 1, cat: "restaurant", desc: "Bakery & café — pastries, açaí bowls, Kauai coffee" },
        { lat: 22.1364, lng: -159.6631, label: "Na Pali Coast", num: 2, cat: "attraction", desc: "Dramatic 3,000-ft sea cliffs — catamaran cruise highlight" },
        { lat: 22.2074, lng: -159.5058, label: "Bar Acuda", num: 3, cat: "restaurant", desc: "Tapas bar — locally sourced small plates & great wine" },
        { lat: 22.2097, lng: -159.5014, label: "Hanalei Pier (Fireworks)", num: 4, cat: "attraction", desc: "July 4th fireworks over Hanalei Bay" },
        { lat: 22.2072, lng: -159.5082, label: "Tahiti Nui", num: 5, cat: "nightlife", desc: "Iconic tiki bar — live music & mai tais" }
      ]
    },
    {
      num: 3,
      neighborhoods: "Tunnels Beach · Limahuli Garden · Ke'e Beach",
      title: "Gardens, Reefs & a Secret Beach",
      description: "Explore the end of the road — where the Na Pali wilderness begins. Snorkel pristine reefs, wander a botanical paradise, and share one last unforgettable sunset.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Tunnels Beach (Makua Beach) Snorkeling",
              description: "One of Kauai's best snorkeling spots — a vast coral reef sheltered by an outer reef that creates calm, crystal-clear lagoons. Swim among tropical fish, sea turtles, and vibrant coral gardens. The dramatic backdrop of Bali Hai makes it surreal.",
              details: [
                "📍 Park along the unmarked dirt road — arrive before 9 AM for a spot",
                "🐢 Green sea turtles are common — keep 10 ft distance (it's the law)",
                "🤿 Calm summer conditions make this ideal for all skill levels"
              ]
            }
          ],
          tips: [
            { type: "tip", text: "There are no facilities at Tunnels — bring water, snacks, and everything you need. That's part of its charm." }
          ]
        },
        {
          label: "Late Morning",
          activities: [
            {
              title: "Limahuli Garden & Preserve",
              description: "A living museum of Hawaiian ethnobotany tucked into a dramatic valley. Ancient taro terraces, rare native plants, and sweeping views of the Na Pali coastline. The self-guided tour is meditative and deeply romantic — you'll often have entire sections to yourselves.",
              details: [
                "🎫 $50/person · Self-guided tour ~1.5 hours",
                "🌿 Part of the National Tropical Botanical Garden",
                "📸 The upper terraces have staggering ocean views"
              ]
            }
          ]
        },
        {
          label: "Afternoon",
          meals: [
            {
              type: "🌮 Lunch",
              name: "Hanalei Taro & Juice Co.",
              description: "Casual food truck serving taro-based dishes — try the taro burger and fresh lilikoi juice. Local, affordable, and uniquely Hawaiian.",
              meta: "$ · Cash preferred · Hanalei Town"
            }
          ],
          activities: [
            {
              title: "Couples Spa at The St. Regis / 1 Hotel Hanalei Bay",
              description: "Treat yourselves to a couples massage at the luxurious Hanalei Bay resort spa. Hawaiian lomi lomi massage uses long flowing strokes inspired by ocean waves. Book the outdoor cabana for garden views.",
              details: [
                "💆 Book 1–2 weeks ahead · ~$250–350/person for 60-min treatment",
                "🌺 Request plumeria-scented oils for the full Hawaiian experience"
              ]
            }
          ]
        },
        {
          label: "Evening",
          activities: [
            {
              title: "Ke'e Beach Sunset",
              description: "Drive to the literal end of the road — Ke'e Beach at Ha'ena State Park. This small, secluded beach sits at the base of the Na Pali cliffs. Watch the sun dip into the Pacific with nobody else around. It's the most dramatic sunset on Kauai and the perfect way to close your trip.",
              details: [
                "🎫 Ha'ena State Park requires a parking reservation (gohaena.com) — book days ahead",
                "🌅 Arrive by 6 PM for golden hour · Sunset ~7:10 PM",
                "🥂 Pack a small picnic and a bottle of sparkling wine"
              ]
            }
          ],
          meals: [
            {
              type: "🍽️ Farewell Dinner",
              name: "Opakapaka Grill & Bar (Princeville)",
              description: "Elevated Hawaiian cuisine with ocean views in Princeville. Fresh opakapaka (pink snapper), Kauai shrimp, and craft cocktails. A refined but relaxed final evening together.",
              meta: "$$$ · Reservations recommended · 10-min drive from Hanalei"
            }
          ]
        }
      ],
      mapPins: [
        { lat: 22.2219, lng: -159.5674, label: "Tunnels Beach", num: 1, cat: "beach", desc: "Premier snorkeling — coral reef lagoons & sea turtles" },
        { lat: 22.2189, lng: -159.5781, label: "Limahuli Garden", num: 2, cat: "attraction", desc: "Botanical garden — ancient terraces & Na Pali views" },
        { lat: 22.2082, lng: -159.5043, label: "Hanalei Taro & Juice Co.", num: 3, cat: "restaurant", desc: "Local food truck — taro burgers & lilikoi juice" },
        { lat: 22.2217, lng: -159.5134, label: "1 Hotel Hanalei Bay Spa", num: 4, cat: "spa", desc: "Couples lomi lomi massage — luxury resort spa" },
        { lat: 22.2206, lng: -159.5857, label: "Ke'e Beach", num: 5, cat: "beach", desc: "End-of-the-road beach — most dramatic sunset on Kauai" },
        { lat: 22.2178, lng: -159.4887, label: "Opakapaka Grill & Bar", num: 6, cat: "restaurant", desc: "Elevated Hawaiian cuisine — ocean views in Princeville" }
      ]
    }
  ],

  budgetTable: [
    { category: "Accommodation (3 nights)", budget: "$600–$1,200", mid: "$900–$1,800", premium: "$1,500–$3,000" },
    { category: "Na Pali Catamaran Cruise", budget: "$200/pp", mid: "$200/pp", premium: "$350/pp (private)" },
    { category: "Dining (3 days)", budget: "$200–$300", mid: "$400–$500", premium: "$600+" },
    { category: "Car Rental (3 days)", budget: "$150–$200", mid: "$200–$300", premium: "$300+" },
    { category: "Spa (couples)", budget: "—", mid: "$400–$600", premium: "$700+" },
    { category: "Activities & Park Fees", budget: "$100–$150", mid: "$150–$200", premium: "$200+" },
    { category: "Total (2 people)", budget: "$1,250–$2,050", mid: "$2,250–$3,700", premium: "$3,650–$7,050" }
  ],

  practicalInfo: [
    {
      title: "🛫 Getting There",
      items: [
        "Fly into Lihue Airport (LIH) — direct flights from LAX, SFO, SEA, and most West Coast hubs",
        "Rent a car at the airport — Turo often has better rates than the big agencies",
        "Drive north on Kuhio Highway (Hwy 56 → 560) — about 40 minutes to Hanalei",
        "The one-lane bridges after Princeville are charming — yield to oncoming traffic, embrace the slow pace"
      ]
    },
    {
      title: "🏠 Where to Stay",
      items: [
        "<strong>Romantic splurge:</strong> 1 Hotel Hanalei Bay (formerly St. Regis) — cliffside luxury overlooking the bay",
        "<strong>Cozy & private:</strong> Hanalei Colony Resort — beachfront units at the end of the road in Ha'ena, no TVs or phones",
        "<strong>Vacation rental:</strong> VRBO/Airbnb in Hanalei or Princeville — look for places with mountain or ocean views",
        "Stay North Shore — Princeville to Ha'ena. Don't stay in Poipu/Lihue; the commute kills the vibe."
      ]
    },
    {
      title: "🌴 Good to Know",
      items: [
        "Ha'ena State Park (Ke'e Beach, Kalalau Trail) requires advance reservations at <strong>gohaena.com</strong>",
        "North Shore has limited dining — don't wait until 8 PM to figure out dinner",
        "Grocery run at Big Save in Hanalei or Foodland in Princeville upon arrival",
        "Mosquito repellent for garden visits and trail walks",
        "July is peak season — book accommodation and the Na Pali cruise ASAP"
      ]
    }
  ],

  highlights: [
    "Na Pali Coast catamaran cruise along 3,000-ft sea cliffs",
    "July 4th fireworks over Hanalei Bay",
    "Snorkeling with sea turtles at Tunnels Beach",
    "Sunset at Ke'e Beach — the end of the road",
    "Couples spa at 1 Hotel Hanalei Bay",
    "Candlelit dinner at Mediterraneo"
  ]
};

const result = fulfillOrder(order, itineraryData);
console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
