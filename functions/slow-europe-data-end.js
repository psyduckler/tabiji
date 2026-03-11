// Days 12 (pins), 13, 14, plus itineraryData wrapper and execution

const day12pins = [
  { lat: 41.3874, lng: 2.1686, label: "Barcelona Sants", num: 1, cat: "transport", desc: "Main station — Metro to Gothic Quarter in 10 min" },
  { lat: 41.3839, lng: 2.1767, label: "Barri Gotic", num: 2, cat: "neighborhood", desc: "Medieval heart — narrow lanes, tapas, cathedral" },
  { lat: 41.3851, lng: 2.1734, label: "La Rambla", num: 3, cat: "walk", desc: "Famous boulevard to the waterfront" },
  { lat: 41.3825, lng: 2.1828, label: "El Born", num: 4, cat: "neighborhood", desc: "Trendy — Picasso Museum, cocktails, boutiques" }
];

const day13 = {
  num: 13, title: "Barcelona — Gaudi, Gothic Quarter & Waterfront",
  neighborhoods: "Sagrada Familia · Eixample · Barri Gotic · El Born",
  description: "Full day in Barcelona. Gaudi's masterpieces, medieval lanes, and a tapas crawl through El Born.",
  timeBlocks: [
    {
      label: "Morning",
      activities: [{
        title: "Sagrada Familia",
        description: "Book timed entry weeks ahead — it ALWAYS sells out. Gaudi's unfinished basilica is genuinely one of the most extraordinary buildings on Earth. The interior with tree-like columns and stained glass light show is unlike anything else.",
        details: ["Entry: 26 euros, book online weeks ahead", "Go at opening (9am) for the best light through the stained glass"]
      }],
      meals: [], tips: []
    },
    {
      label: "Afternoon",
      activities: [
        {
          title: "Gaudi on Passeig de Gracia",
          description: "Walk through Eixample to Casa Batllo (dragon-back roof, bone facade) and La Pedrera/Casa Mila (undulating stone, rooftop warriors). Two of Gaudi's residential masterpieces, side by side on Barcelona's grandest boulevard.",
          details: ["Casa Batllo: 35 euros", "La Pedrera: 25 euros, rooftop at sunset is best"]
        },
        {
          title: "Gothic Quarter & El Born",
          description: "The medieval heart of Barcelona — the Cathedral, Placa del Rei, narrow lanes opening into hidden squares. Then into El Born for the Picasso Museum and the best tapas bars in the city.",
          details: []
        }
      ],
      meals: [{
        type: "Dinner", name: "Tapas Crawl in El Born",
        description: "Pintxos, patatas bravas, pan con tomate, jamon iberico, and vermouth. Hit 3-4 bars — each one has a specialty.",
        meta: "El Born · 25-40 euros"
      }],
      tips: [{ type: "tip", text: "La Boqueria market on La Rambla is a tourist trap at the front — walk to the back stalls for the real stuff. Or skip it and go to Mercat de Santa Caterina in El Born instead." }]
    }
  ],
  mapPins: [
    { lat: 41.4036, lng: 2.1744, label: "Sagrada Familia", num: 1, cat: "sight", desc: "Gaudi's masterpiece — most extraordinary basilica on Earth" },
    { lat: 41.3917, lng: 2.1650, label: "Casa Batllo", num: 2, cat: "sight", desc: "Dragon-back roof, bone facade" },
    { lat: 41.3953, lng: 2.1620, label: "La Pedrera", num: 3, cat: "sight", desc: "Undulating building with warrior chimney rooftop" },
    { lat: 41.3841, lng: 2.1718, label: "La Boqueria Market", num: 4, cat: "market", desc: "Famous food market — fresh juice, jamon, seafood" }
  ]
};

const day14 = {
  num: 14, title: "Barcelona — Park Guell, Montjuic & Departure",
  neighborhoods: "Park Guell · Montjuic · Poble Sec",
  description: "Final day. Gaudi's mosaic wonderland, hilltop views, and a final vermouth. 14 days, 4 countries, 3,500km — zero flights.",
  timeBlocks: [
    {
      label: "Morning",
      activities: [{
        title: "Park Guell",
        description: "Gaudi's mosaic wonderland overlooking the city. The tiled bench terrace has the best panoramic view of Barcelona with the sea behind. Book timed entry (10 euros) and go at opening for fewer crowds.",
        details: ["10 euros, timed entry required", "Go at 9:30am opening — the main terrace fills up fast"]
      }],
      meals: [], tips: []
    },
    {
      label: "Afternoon",
      activities: [
        {
          title: "Montjuic Hill",
          description: "Funicular or cable car up for sweeping views of the port and city. Visit the Fundacio Joan Miro — one of Spain's best modern art museums. Walk through the gardens and the Poble Sec neighborhood below for a final vermouth.",
          details: ["Cable car: 13 euros round trip", "Fundacio Joan Miro: 14 euros"]
        }
      ],
      meals: [{
        type: "Lunch", name: "Vermouth & Tapas in Poble Sec",
        description: "The local neighborhood below Montjuic — vermouth bars, tapas joints, and zero tourists. The perfect final meal of the trip.",
        meta: "Poble Sec · 15-25 euros"
      }],
      tips: [{ type: "tip", text: "Final stats: 14 days, 4 countries (France, Switzerland, Italy, Spain), roughly 3,500km of track, and zero flights. That is slow travel done right." }]
    }
  ],
  mapPins: [
    { lat: 41.4145, lng: 2.1527, label: "Park Guell", num: 1, cat: "sight", desc: "Gaudi's mosaic wonderland — panoramic city views" },
    { lat: 41.3688, lng: 2.1600, label: "Montjuic", num: 2, cat: "sight", desc: "Hilltop — cable car, castle, gardens, port views" },
    { lat: 41.3686, lng: 2.1598, label: "Fundacio Joan Miro", num: 3, cat: "museum", desc: "Miro's art in a stunning Sert building" },
    { lat: 41.3731, lng: 2.1640, label: "Poble Sec", num: 4, cat: "neighborhood", desc: "Local area below Montjuic — vermouth bars, chill vibes" }
  ]
};

module.exports = { day12pins, day13, day14 };
