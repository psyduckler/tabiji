const DESTINATIONS = [
    {
        id: "tokyo",
        name: "Tokyo, Japan",
        icon: "🗼",
        tagline: "Neon chaos meets ancient temples",
        vibes: ["adventure", "culture", "foodie"],
        budget: "mid",
        energy: "high",
        idealDuration: ["week", "extended"],
        activities: [
            "Get lost in the sensory overload of Shibuya Crossing",
            "Hunt for the best ramen in a 6-seat basement shop",
            "Visit a cat cafe (or owl cafe, if you're chaotic)",
            "Explore Senso-ji Temple at dawn before the crowds",
            "Arcade hop through Akihabara until 3am"
        ],
        food: [
            "Tsukiji Outer Market for fresh sushi breakfast",
            "Convenience store onigiri (surprisingly elite)",
            "Izakaya hopping in Yurakucho under the train tracks"
        ],
        stay: "Shinjuku area - walkable to everything, maximum chaos",
        tabijiComment: "In Tokyo, ancient wisdom and neon dreams dance together. The city teaches patience in chaos — a profound lesson for any traveler."
    },
    {
        id: "lisbon",
        name: "Lisbon, Portugal",
        icon: "🚃",
        tagline: "Hills, tiles, and existential melancholy",
        vibes: ["culture", "relaxation", "foodie"],
        budget: "low",
        energy: "medium",
        idealDuration: ["weekend", "week"],
        activities: [
            "Ride Tram 28 like a local (stand, don't sit)",
            "Get lost in Alfama's winding streets",
            "Watch sunset from Miradouro da Senhora do Monte",
            "Day trip to Sintra's fairy tale palaces",
            "Listen to Fado music and feel things"
        ],
        food: [
            "Pastéis de Belém - the custard tart pilgrimage",
            "Bifana sandwiches at a local tasca",
            "Fresh seafood at Cervejaria Ramiro"
        ],
        stay: "Baixa or Bairro Alto - central, walkable, very steep",
        tabijiComment: "Lisbon's hills are a metaphor, young traveler. The climb is hard, but the view rewards those who persist. Fado will teach you that beauty lives in longing."
    },
    {
        id: "bali",
        name: "Bali, Indonesia",
        icon: "🌴",
        tagline: "Rice terraces, temples, and transformation",
        vibes: ["relaxation", "adventure", "spiritual"],
        budget: "low",
        energy: "medium",
        idealDuration: ["week", "extended"],
        activities: [
            "Sunrise hike up Mount Batur",
            "Get a $10 massage that changes your life",
            "Explore Ubud's rice terraces and art scene",
            "Snorkel or dive at Nusa Penida",
            "Temple hop: Uluwatu, Tirta Empul, Tanah Lot"
        ],
        food: [
            "Nasi goreng from a warung (street stall)",
            "Smoothie bowls in Canggu (basic but good)",
            "Babi guling (suckling pig) if you're adventurous"
        ],
        stay: "Ubud for culture, Canggu for beaches, Seminyak for nightlife",
        tabijiComment: "Bali whispers to those who listen. Beneath the tourist bustle lies deep spiritual current. Let the rice terraces remind you that growth takes time."
    },
    {
        id: "iceland",
        name: "Reykjavik, Iceland",
        icon: "🌋",
        tagline: "Volcanoes, waterfalls, and expensive hot dogs",
        vibes: ["adventure", "nature"],
        budget: "high",
        energy: "high",
        idealDuration: ["week", "extended"],
        activities: [
            "Drive the Golden Circle (Geysir, Gullfoss, Thingvellir)",
            "Soak in a geothermal pool that isn't Blue Lagoon",
            "Chase waterfalls on the South Coast",
            "Northern Lights hunt (October-March, luck required)",
            "Hike a glacier before they're all gone"
        ],
        food: [
            "Bæjarins Beztu hot dogs (trust the process)",
            "Lamb soup to warm your frozen soul",
            "Skip the fermented shark unless you hate yourself"
        ],
        stay: "Reykjavik downtown - everything else is a long drive",
        tabijiComment: "Iceland reveals Earth's raw power. Fire and ice coexist here, teaching us that opposites need not conflict. Let the northern lights humble your spirit."
    },
    {
        id: "mexico-city",
        name: "Mexico City, Mexico",
        icon: "🌮",
        tagline: "Tacos, murals, and controlled chaos",
        vibes: ["culture", "foodie", "adventure"],
        budget: "low",
        energy: "high",
        idealDuration: ["weekend", "week"],
        activities: [
            "Explore the murals at Palacio de Bellas Artes",
            "Wander through Coyoacán and visit Frida's house",
            "Sunday at Chapultepec Park like a local",
            "Lucha Libre wrestling (go for the spectacle)",
            "Day trip to Teotihuacán pyramids"
        ],
        food: [
            "Taco crawl through Roma Norte",
            "Churros and chocolate at El Moro",
            "Mezcal tasting in Mezcalería"
        ],
        stay: "Roma or Condesa - trendy, walkable, excellent food scene",
        tabijiComment: "Mexico City pulses with the heartbeat of civilizations past and present. Here, every taco tells a story, every mural holds a revolution. Listen closely."
    },
    {
        id: "new-zealand",
        name: "South Island, New Zealand",
        icon: "🏔️",
        tagline: "Lord of the Rings but you're the hobbit",
        vibes: ["adventure", "nature"],
        budget: "high",
        energy: "high",
        idealDuration: ["extended"],
        activities: [
            "Hike the Routeburn or Milford Track",
            "Bungee jump in Queenstown (or watch others)",
            "Kayak Milford Sound at dawn",
            "Stargazing at Lake Tekapo Dark Sky Reserve",
            "Road trip the entire island (2 weeks minimum)"
        ],
        food: [
            "Fergburger in Queenstown (worth the line)",
            "Fish and chips by any harbor",
            "Flat whites - they invented them here"
        ],
        stay: "Queenstown as a base, but keep moving",
        tabijiComment: "New Zealand's mountains do not move, yet they transform all who gaze upon them. Nature here is the oldest teacher — approach with reverence."
    },
    {
        id: "barcelona",
        name: "Barcelona, Spain",
        icon: "🎭",
        tagline: "Gaudí's fever dreams and 2am dinners",
        vibes: ["culture", "foodie", "relaxation"],
        budget: "mid",
        energy: "medium",
        idealDuration: ["weekend", "week"],
        activities: [
            "Get overwhelmed by Sagrada Família",
            "Wander Park Güell early morning",
            "Beach day at Barceloneta (watch your stuff)",
            "Gothic Quarter exploration without a map",
            "Watch sunset from Bunkers del Carmel"
        ],
        food: [
            "La Boqueria market grazing",
            "Patatas bravas bar hop",
            "Vermouth hour (it's a thing, embrace it)"
        ],
        stay: "El Born or Gràcia - local vibes, excellent food",
        tabijiComment: "Barcelona flows on its own rhythm. Gaudí understood that nature's curves hold more truth than straight lines. Let the city teach you to slow down."
    },
    {
        id: "morocco",
        name: "Marrakech, Morocco",
        icon: "🕌",
        tagline: "Sensory overload in the best way",
        vibes: ["adventure", "culture"],
        budget: "low",
        energy: "high",
        idealDuration: ["weekend", "week"],
        activities: [
            "Get lost in the Medina (you will, accept it)",
            "Haggle in the souks for things you don't need",
            "Jardin Majorelle for a breath of calm",
            "Day trip to the Atlas Mountains",
            "Rooftop sunset with mint tea"
        ],
        food: [
            "Tagine everything",
            "Street food in Jemaa el-Fnaa square",
            "Fresh orange juice for 50 cents"
        ],
        stay: "A riad in the Medina - traditional courtyard house",
        tabijiComment: "Marrakech tests your senses and rewards your patience. In the maze of the Medina, getting lost is the first step to finding what you seek."
    },
    {
        id: "kyoto",
        name: "Kyoto, Japan",
        icon: "⛩️",
        tagline: "The quiet sibling Tokyo doesn't talk about",
        vibes: ["culture", "relaxation", "spiritual"],
        budget: "mid",
        energy: "low",
        idealDuration: ["weekend", "week"],
        activities: [
            "Fushimi Inari at 5am (trust me on the timing)",
            "Bamboo grove in Arashiyama",
            "Tea ceremony experience",
            "Wander Gion and spot a geiko",
            "Temple meditation at a Zen garden"
        ],
        food: [
            "Kaiseki multi-course dinner (splurge once)",
            "Matcha everything in Uji",
            "Nishiki Market snacking"
        ],
        stay: "Near Gion or a traditional ryokan experience",
        tabijiComment: "Kyoto preserves what Tokyo races past. In the silence between temple bells, wisdom waits for those patient enough to hear it."
    },
    {
        id: "colombia",
        name: "Medellín, Colombia",
        icon: "☕",
        tagline: "Eternal spring and reinvention",
        vibes: ["adventure", "culture", "foodie"],
        budget: "low",
        energy: "high",
        idealDuration: ["week", "extended"],
        activities: [
            "Ride the cable cars over the comunas",
            "Street art tour through Comuna 13",
            "Day trip to Guatapé and climb El Peñol",
            "Coffee farm tour in the hills",
            "Salsa dancing (you'll be bad, that's okay)"
        ],
        food: [
            "Bandeja paisa (the mountain of food)",
            "Empanadas from any street corner",
            "Fresh fruit juices you've never heard of"
        ],
        stay: "El Poblado or Laureles - safe, walkable, great food",
        tabijiComment: "Medellín proves that transformation is always possible. From darkness to eternal spring — a city that chose to bloom again. There is hope in every corner."
    }
];

const NPC_EXPRESSIONS = {
    neutral: `
       ╭───────╮
       │ ◉   ◉ │
       │  ╭▽╮  │
       │  ╰─╯  │
      ╭┴───────┴╮
     ╱    |||    ╲
    ╱    (   )    ╲
    ╰──────────────╯`,
    thinking: `
       ╭───────╮
       │ ◉   ◉ │
       │  ╭▽╮  │  ?
       │  ╰─╯  │
      ╭┴───────┴╮
     ╱    |||    ╲
    ╱    (   )    ╲
    ╰──────────────╯`,
    excited: `
       ╭───────╮
       │ ★   ★ │
       │  ╭▽╮  │
       │  ╰▽╯  │
     ~╭┴───────┴╮~
     ╱    |||    ╲
    ╱    (   )    ╲
    ╰──────────────╯`,
    judging: `
       ╭───────╮
       │ ◉   ─ │
       │  ╭▽╮  │
       │  ╰─╯  │
      ╭┴───────┴╮
     ╱    |||    ╲
    ╱    (   )    ╲
    ╰──────────────╯`,
    smug: `
       ╭───────╮
       │ ─   ─ │
       │  ╭▽╮  │
       │  ╰◡╯  │
      ╭┴───────┴╮
     ╱    |||    ╲
    ╱    (   )    ╲
    ╰──────────────╯`
};
