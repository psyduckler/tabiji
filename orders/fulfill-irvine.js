const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: "order_1771789018949_kt4ydt",
  email: "klabianco+testingtravel@gmail.com",
  destination: "irvine, ca",
  start_date: "2026-02-22",
  end_date: "2026-02-28"
};

const itineraryData = {
  destination: "Irvine, California",
  countryEmoji: "🇺🇸",
  title: "Irvine & Orange County: Sun, Culture & Coastal Bliss",
  subtitle: "A week in Southern California's most livable city — from world-class parks to Pacific sunsets",
  description: "Irvine sits at the heart of Orange County, blending master-planned green spaces with an incredible international dining scene, easy beach access, and outdoor adventures. This 7-day itinerary takes your group from the Great Park balloon ride to Crystal Cove tide pools, through Irvine's legendary Asian food corridor, and out to the coastal villages of Laguna and Newport.",
  duration: "7 days",
  dates: "Feb 22 – 28, 2026",
  budget: "$$",
  pace: "Relaxed",
  bestFor: "Groups · Foodies · Outdoor Lovers",

  essentials: [
    { title: "🚗 Getting Around", text: "A car is essential in Irvine. Rideshare works for nights out but you'll want wheels for day trips to the coast and parks. Street parking is plentiful; most attractions have free lots." },
    { title: "🌤️ February Weather", text: "Expect highs around 65-70°F and lows near 50°F. Rain is possible but rare. Layer up for cool mornings — it warms up fast by noon." },
    { title: "🍜 The Food Scene", text: "Irvine has one of the best Asian food corridors in the US. Diamond Jamboree and the Culver Plaza area are packed with Korean BBQ, Vietnamese pho, Taiwanese boba, and Japanese ramen. Don't sleep on it." },
    { title: "🏖️ Beach Access", text: "Newport Beach and Crystal Cove are 15-20 min from central Irvine. Laguna Beach is 25 min. No beach parking fees in winter but lots fill by 11am on weekends." }
  ],

  days: [
    {
      num: 1,
      neighborhoods: "Orange County Great Park · Woodbury",
      title: "Arrival & The Great Park",
      description: "Settle in, then explore Irvine's crown jewel — the 1,300-acre Great Park built on the former El Toro Marine base.",
      timeBlocks: [
        {
          label: "Afternoon",
          activities: [
            {
              title: "Orange County Great Park",
              description: "Start with the iconic Great Park Balloon — a tethered helium balloon that rises 400 feet for panoramic views of the Santa Ana Mountains and the Pacific. Then explore the farm, playground, and art galleries.",
              details: [
                "Great Park Balloon rides are free — first come, first served, weekends 10am-5pm",
                "Check the sports complex and carousel too — all free",
                "The Farmers Market runs Sundays 10am-2pm if you're here on a Sunday"
              ]
            }
          ],
          tips: [
            { type: "tip", text: "The balloon doesn't fly if winds exceed 25mph — call ahead to check." }
          ]
        },
        {
          label: "Evening",
          meals: [
            {
              type: "Dinner",
              name: "TEN Ramen",
              description: "Rich, deeply flavored tonkotsu ramen with perfectly chewy noodles. The spicy miso is outstanding.",
              meta: "Woodbury Town Center · $12-16/bowl · Casual"
            }
          ],
          tips: [
            { type: "reddit", text: "TEN Ramen is the best ramen in Irvine, hands down. Get the black garlic tonkotsu.", cite: "r/orangecounty" }
          ]
        }
      ],
      mapPins: [
        { lat: 33.6603, lng: -117.7682, label: "Orange County Great Park", num: 1, cat: "attraction", desc: "1,300-acre park with free balloon rides and gardens" },
        { lat: 33.6948, lng: -117.7578, label: "TEN Ramen", num: 2, cat: "food", desc: "Top-rated ramen in Irvine" }
      ]
    },
    {
      num: 2,
      neighborhoods: "Diamond Jamboree · UCI · Turtle Rock",
      title: "Food Crawl & University Culture",
      description: "Dive into Irvine's legendary Asian food scene, then explore the UCI campus and its world-class art museum.",
      timeBlocks: [
        {
          label: "Morning",
          meals: [
            {
              type: "Brunch",
              name: "85°C Bakery Cafe",
              description: "Taiwanese bakery chain that started in Irvine. Sea salt coffee is iconic. Grab egg tarts, brioche, and their famous marble taro bread.",
              meta: "Diamond Jamboree · $3-8 · Casual"
            }
          ]
        },
        {
          label: "Midday",
          activities: [
            {
              title: "Diamond Jamboree Food Crawl",
              description: "This open-air plaza is ground zero for Irvine's food scene. Walk between a dozen incredible Asian restaurants — from hand-pulled noodles to Korean fried chicken.",
              details: [
                "Must-try: A&J Restaurant (Taiwanese beef noodle soup), Boiling Point (hot pot), Curry House",
                "Boba stop: Ding Tea or Tiger Sugar for brown sugar boba",
                "Come hungry — you'll want to split dishes across 2-3 spots"
              ]
            }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "UCI Campus & Langson IMCA",
              description: "Stroll the beautiful UC Irvine campus — the Aldrich Park ring road is a peaceful walk through eucalyptus groves. Visit the Jack and Shanaz Langson Institute and Museum of California Art (IMCA) for rotating contemporary exhibitions.",
              details: [
                "IMCA is free admission — check current exhibitions at imca.uci.edu",
                "The campus has striking brutalist architecture worth photographing"
              ]
            }
          ]
        },
        {
          label: "Evening",
          meals: [
            {
              type: "Dinner",
              name: "Baekjeong Korean BBQ",
              description: "Premium Korean BBQ with attentive tableside grilling. The combo galbi and pork belly set is perfect for groups.",
              meta: "Irvine · $30-40/person · Reservations recommended"
            }
          ]
        }
      ],
      mapPins: [
        { lat: 33.6516, lng: -117.8387, label: "Diamond Jamboree", num: 1, cat: "food", desc: "Asian food plaza with 12+ restaurants" },
        { lat: 33.6461, lng: -117.8427, label: "UCI Campus", num: 2, cat: "attraction", desc: "University campus with Langson IMCA museum" },
        { lat: 33.6568, lng: -117.8302, label: "Baekjeong Korean BBQ", num: 3, cat: "food", desc: "Premium Korean BBQ" }
      ]
    },
    {
      num: 3,
      neighborhoods: "Crystal Cove · Newport Coast · Laguna Beach",
      title: "Coastal Day — Crystal Cove to Laguna",
      description: "Head to the coast for tide pools, a historic beach village, and the art galleries of Laguna Beach.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Crystal Cove State Park",
              description: "This 3.2-mile stretch of coastline is one of the last undeveloped spots on the Orange County coast. Explore tide pools at low tide, hike the bluffs, or just beachcomb.",
              details: [
                "Parking: $15/day at the beach lot, free along PCH if you walk down",
                "Check tide charts — low tide reveals incredible tide pools at Reef Point",
                "The Historic District has restored 1930s beach cottages you can peek into"
              ]
            }
          ]
        },
        {
          label: "Midday",
          meals: [
            {
              type: "Lunch",
              name: "The Beachcomber Cafe",
              description: "Right on Crystal Cove beach with ocean views. Fresh fish tacos and acai bowls while your feet are still sandy.",
              meta: "Crystal Cove Historic District · $15-25 · Casual beachside"
            }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Laguna Beach Art Walk",
              description: "Drive down PCH to Laguna Beach and wander the downtown gallery district. Over 100 galleries line the streets — from fine art to surf photography.",
              details: [
                "Free to browse — start at Forest Ave and work toward the coast",
                "Stop at Heisler Park for dramatic cliffside views and a short coastal trail",
                "Main Beach is great for people-watching"
              ]
            }
          ],
          tips: [
            { type: "tip", text: "February is the quiet season in Laguna — you'll have galleries mostly to yourself." }
          ]
        },
        {
          label: "Evening",
          meals: [
            {
              type: "Dinner",
              name: "Nick's Laguna Beach",
              description: "Upscale California cuisine with an incredible ocean-view patio. The seared ahi and filet mignon are standouts.",
              meta: "Laguna Beach · $35-55/person · Reservations essential"
            }
          ]
        }
      ],
      mapPins: [
        { lat: 33.5734, lng: -117.8401, label: "Crystal Cove State Park", num: 1, cat: "nature", desc: "Pristine coastline with tide pools" },
        { lat: 33.5726, lng: -117.8363, label: "The Beachcomber Cafe", num: 2, cat: "food", desc: "Beachside dining at Crystal Cove" },
        { lat: 33.5427, lng: -117.7854, label: "Laguna Beach Downtown", num: 3, cat: "attraction", desc: "Art galleries and coastal charm" },
        { lat: 33.5433, lng: -117.7872, label: "Nick's Laguna Beach", num: 4, cat: "food", desc: "Upscale ocean-view dining" }
      ]
    },
    {
      num: 4,
      neighborhoods: "Bommer Canyon · Turtle Rock · Irvine Spectrum",
      title: "Hiking & Shopping",
      description: "Hit the trails in the morning, then spend the afternoon at one of SoCal's best outdoor shopping destinations.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Bommer Canyon Trail",
              description: "A moderate 4.5-mile loop through coastal sage scrub with views of the valley. You might spot coyotes, hawks, or even a bobcat.",
              details: [
                "Trailhead at the end of Shady Canyon Dr — free parking",
                "Bring water and sunscreen — exposed trail with little shade",
                "Best started before 10am to beat the heat"
              ]
            }
          ],
          meals: [
            {
              type: "Breakfast",
              name: "Sidecar Doughnuts",
              description: "Artisan doughnuts made fresh daily. The huckleberry and brown butter are cult favorites.",
              meta: "Woodbury · $4-6/doughnut · Grab & go"
            }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Irvine Spectrum Center",
              description: "More than a mall — this 93-acre outdoor center has a giant Ferris wheel, IMAX theater, and over 150 shops and restaurants under the signature Moorish-inspired architecture.",
              details: [
                "Ride the Giant Wheel for sweeping OC views ($12/person)",
                "Catch a movie at the Regal IMAX — recliners and massive screen",
                "Browse Barnes & Noble, lululemon, and Apple"
              ]
            }
          ]
        },
        {
          label: "Evening",
          meals: [
            {
              type: "Dinner",
              name: "North Italia",
              description: "Handmade pasta and wood-fired pizza in a stylish setting. The short rib radiatori and Margherita pizza are crowd favorites.",
              meta: "Irvine Spectrum · $20-35/person · Reservations recommended"
            }
          ],
          tips: [
            { type: "reddit", text: "North Italia at the Spectrum is consistently good. The truffle garlic bread appetizer is a must.", cite: "r/orangecounty" }
          ]
        }
      ],
      mapPins: [
        { lat: 33.6148, lng: -117.8080, label: "Bommer Canyon Trailhead", num: 1, cat: "nature", desc: "4.5-mile loop with canyon views" },
        { lat: 33.6494, lng: -117.7440, label: "Irvine Spectrum Center", num: 2, cat: "attraction", desc: "Major outdoor shopping & entertainment" },
        { lat: 33.6498, lng: -117.7436, label: "North Italia", num: 3, cat: "food", desc: "Handmade pasta at the Spectrum" }
      ]
    },
    {
      num: 5,
      neighborhoods: "Newport Beach · Balboa Island · Corona del Mar",
      title: "Newport Beach Day",
      description: "Explore the classic OC beach town — from the Balboa Peninsula boardwalk to the charming shops of Balboa Island.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Balboa Island & Ferry",
              description: "Take the tiny Balboa Island Ferry ($1.50/person) across the harbor. Walk the perimeter path with bay views, then hit Marine Avenue for the famous Balboa Bar — a frozen banana dipped in chocolate.",
              details: [
                "Park on the peninsula side and take the ferry over — it's part of the fun",
                "Dad's Donuts and Sugar 'n Spice are island institutions",
                "Walk the full island perimeter — about 1.5 miles with gorgeous harbor views"
              ]
            }
          ]
        },
        {
          label: "Midday",
          meals: [
            {
              type: "Lunch",
              name: "Bear Flag Fish Company",
              description: "The freshest fish in Newport. Order the poke bowl or grilled fish tacos at this counter-service local gem.",
              meta: "Newport Beach · $12-18 · Casual"
            }
          ],
          activities: [
            {
              title: "Newport Beach Pier & Boardwalk",
              description: "Walk the historic pier for ocean views, then stroll the Balboa Peninsula boardwalk. In winter the surf can be dramatic — great for watching from the pier.",
              details: []
            }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Corona del Mar State Beach",
              description: "This quieter, upscale beach has tide pools at Little Corona and calm swimming coves. The viewpoints along Ocean Blvd are postcard-perfect.",
              details: [
                "Free street parking on residential streets above the beach",
                "Walk down to Little Corona for the best tide pools"
              ]
            }
          ]
        },
        {
          label: "Evening",
          meals: [
            {
              type: "Dinner",
              name: "Habana",
              description: "Cuban-inspired cocktails and Latin fusion food in a cozy, vibrant setting. The mojitos are legendary.",
              meta: "Costa Mesa (nearby) · $25-40/person · Great cocktails"
            }
          ]
        }
      ],
      mapPins: [
        { lat: 33.6075, lng: -117.8965, label: "Balboa Island", num: 1, cat: "attraction", desc: "Charming island with ferry and Balboa Bars" },
        { lat: 33.6050, lng: -117.9297, label: "Newport Beach Pier", num: 2, cat: "attraction", desc: "Historic pier with ocean views" },
        { lat: 33.5929, lng: -117.8697, label: "Corona del Mar", num: 3, cat: "nature", desc: "Upscale beach with tide pools" },
        { lat: 33.6637, lng: -117.9029, label: "Habana", num: 4, cat: "food", desc: "Cuban-inspired cocktails and dining" }
      ]
    },
    {
      num: 6,
      neighborhoods: "San Juan Capistrano · Dana Point",
      title: "Day Trip — Mission & Harbor",
      description: "Head south to the historic Mission San Juan Capistrano and the laid-back Dana Point Harbor for whale watching season.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Mission San Juan Capistrano",
              description: "Founded in 1776, this is one of California's most beautiful missions. The gardens, ruins of the Great Stone Church, and the Serra Chapel (oldest building in California still in use) are stunning.",
              details: [
                "Admission: $14/adult — self-guided audio tour included",
                "Allow 1.5-2 hours for a thorough visit",
                "The gardens are particularly photogenic in the morning light"
              ]
            }
          ]
        },
        {
          label: "Midday",
          meals: [
            {
              type: "Lunch",
              name: "The Fisherman's Restaurant & Bar",
              description: "Classic harbor seafood spot right on Dana Point Harbor. Clam chowder and fish & chips with marina views.",
              meta: "Dana Point Harbor · $15-25 · Casual waterfront"
            }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Dana Point Whale Watching",
              description: "February is peak whale watching season! Gray whales migrate past Dana Point, and blue whales sometimes appear. Captain Dave's Dolphin & Whale Safari runs 2-hour tours.",
              details: [
                "Book Captain Dave's ($65/person) or Dana Wharf ($49/person)",
                "February-March is peak gray whale season — sighting rates above 90%",
                "Bring layers — it's cooler on the water"
              ]
            }
          ],
          tips: [
            { type: "tip", text: "February is one of the best months for whale watching off the OC coast. Don't skip this." }
          ]
        },
        {
          label: "Evening",
          meals: [
            {
              type: "Dinner",
              name: "Brodard Chateau",
              description: "Upscale Vietnamese in an elegant setting. Famous for their nem nướng (spring rolls) — possibly the best in all of Orange County.",
              meta: "Garden Grove (near Irvine) · $20-35/person · Reservations recommended"
            }
          ],
          tips: [
            { type: "reddit", text: "Brodard's nem nướng is a must. Get the Chateau location — same food, nicer space.", cite: "r/orangecounty" }
          ]
        }
      ],
      mapPins: [
        { lat: 33.5017, lng: -117.6628, label: "Mission San Juan Capistrano", num: 1, cat: "attraction", desc: "Historic 1776 California mission" },
        { lat: 33.4597, lng: -117.6965, label: "Dana Point Harbor", num: 2, cat: "attraction", desc: "Whale watching and waterfront dining" },
        { lat: 33.7789, lng: -117.9625, label: "Brodard Chateau", num: 3, cat: "food", desc: "Upscale Vietnamese with famous spring rolls" }
      ]
    },
    {
      num: 7,
      neighborhoods: "Quail Hill · Culver Plaza · Irvine",
      title: "Last Day — Local Favorites",
      description: "Wrap up the trip with a gentle morning hike, one more incredible meal, and some last-minute exploring.",
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            {
              title: "Quail Hill Loop Trail",
              description: "An easy 2-mile loop with sweeping views of Irvine, Saddleback Mountain, and the Pacific on clear days. Perfect sunrise or morning walk.",
              details: [
                "Trailhead on Shady Canyon Dr — small parking lot, arrive early",
                "Mostly flat with one gentle hill — suitable for all fitness levels",
                "Great bird-watching spot — look for quail, red-tailed hawks"
              ]
            }
          ]
        },
        {
          label: "Midday",
          meals: [
            {
              type: "Brunch",
              name: "Burnt Crumbs",
              description: "Creative comfort food — their Sloppy Joe grilled cheese and ube donut are Instagram famous. Playful, inventive menu.",
              meta: "Irvine Spectrum · $12-18 · Casual"
            }
          ]
        },
        {
          label: "Afternoon",
          activities: [
            {
              title: "Last Boba & Souvenirs",
              description: "Make a final stop at Culver Plaza for one more boba run and any souvenir shopping. 99 Ranch Market is nearby if you want to take home Asian snacks and treats.",
              details: [
                "Omomo Tea Shoppe has the most photogenic boba drinks in Irvine",
                "99 Ranch Market is an experience — massive Asian supermarket with everything"
              ]
            }
          ],
          tips: [
            { type: "tip", text: "Pack some 99 Ranch snacks for the flight home — you won't find this selection elsewhere." }
          ]
        }
      ],
      mapPins: [
        { lat: 33.6260, lng: -117.8030, label: "Quail Hill Loop Trail", num: 1, cat: "nature", desc: "Easy 2-mile loop with panoramic views" },
        { lat: 33.6494, lng: -117.7440, label: "Burnt Crumbs", num: 2, cat: "food", desc: "Creative comfort food at Spectrum" },
        { lat: 33.6841, lng: -117.8268, label: "99 Ranch Market", num: 3, cat: "attraction", desc: "Massive Asian supermarket" }
      ]
    }
  ],

  budgetTable: [
    { category: "Accommodation", budget: "$150-250/night", notes: "Hotels near Spectrum or Great Park" },
    { category: "Food", budget: "$40-70/person/day", notes: "Mix of casual Asian eats and nicer dinners" },
    { category: "Transport", budget: "$40-60/day", notes: "Rental car recommended, or rideshare" },
    { category: "Activities", budget: "$15-65/person", notes: "Most attractions free; whale watching is the splurge" },
    { category: "Total (per person)", budget: "$250-450/day", notes: "For a group of 3-4, sharing accommodation" }
  ],

  practicalInfo: [
    { title: "Getting There", items: ["John Wayne Airport (SNA) is right in Irvine — literally 10 min to most hotels. LAX is 45-60 min depending on traffic. SNA is worth the premium."] },
    { title: "Best Neighborhoods to Stay", items: ["Near Irvine Spectrum for shopping/dining access, or near the Great Park for a quieter base. Both have plenty of hotel options."] },
    { title: "Traffic Warning", items: ["The 405 freeway is brutal during rush hour (7-9am, 4-7pm). Plan coast trips for mid-morning departure.", "Surface streets like Culver, Jeffrey, and Jamboree are your friends."] },
    { title: "Tipping", items: ["Standard 18-20% at sit-down restaurants. Tip $1-2 at boba/coffee shops.", "Whale watching crew typically gets $5-10/person."] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfillment complete:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Fulfillment failed:', err.message);
  process.exit(1);
}
