// Game state
const state = {
    currentStep: 0,
    history: [], // For back button
    answers: {
        vibe: null,
        energy: null,
        budget: null,
        duration: null,
        priority: null
    },
    isTyping: false,
    skipRequested: false
};

// Question order for progress tracking
const QUESTION_ORDER = ['vibe', 'energy', 'budget', 'duration', 'priority'];

// DOM elements
const dialogueText = document.getElementById('dialogue-text');
const dialogueBox = document.getElementById('dialogue-box');
const choicesArea = document.getElementById('choices-area');
const tripResult = document.getElementById('trip-result');
const npcSprite = document.getElementById('npc-sprite');
const progressArea = document.getElementById('progress-area');
const progressLabel = document.getElementById('progress-label');
const navArea = document.getElementById('nav-area');
const backBtn = document.getElementById('back-btn');
const surpriseBtn = document.getElementById('surprise-btn');
const skipHint = document.getElementById('skip-hint');

// Random picker helper
function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

// === DIALOGUE POOLS (50 variants each) ===
const INTRO_TEXTS = [
    "Hoo... welcome, traveler. I am Tabiji.\n\nTell me your heart's yearning, and I shall reveal your path.",
    "Ah, a wanderer approaches. I've been expecting you.\n\nLet us discover where the wind wishes to carry you.",
    "Hoo-hoo! Another soul seeking the horizon.\n\nTell me what stirs your spirit, and I shall guide you.",
    "Welcome, seeker. I am Tabiji, keeper of paths.\n\nShare your desires, and I will read the winds for you.",
    "The feathers sense a curious heart nearby.\n\nCome closer — let me divine your perfect journey.",
    "Hoo... you carry the look of someone ready for adventure.\n\nSpeak, and I shall listen with ancient wisdom.",
    "A traveler! How delightful. I was just preening.\n\nNow then — where shall destiny take you?",
    "The stars told me you'd arrive today.\n\nLet us chart a course through the unknown together.",
    "Hoo... I see wanderlust in your eyes.\n\nTell old Tabiji what your soul craves, and I shall provide.",
    "Another restless spirit finds my perch.\n\nGood. The world has much to show you — let's begin.",
    "Welcome to my branch, traveler.\n\nI've guided thousands to their perfect destination. You're next.",
    "Hoo! A new face! How wonderful.\n\nLet me peer into the winds and find your ideal journey.",
    "*adjusts spectacles*\n\nAh yes, you seek guidance. You've come to the right owl.",
    "The ancient maps whisper your name.\n\nTell me what you seek, and I'll point the way.",
    "Greetings, wanderer. My feathers tingle with possibility.\n\nLet's uncover where you truly belong.",
    "Hoo-hoo... the compass spins for you.\n\nAnswer my questions, and it shall find true north.",
    "A seeker of horizons! My favorite kind of visitor.\n\nLet me help you find the journey you didn't know you needed.",
    "*ruffles feathers wisely*\n\nI am Tabiji. I know every path, every hidden trail. Shall we begin?",
    "The wind carries whispers of your arrival.\n\nTell me your dreams, and I'll weave them into a destination.",
    "Welcome, friend. I've roosted on every continent.\n\nNow let me find the perfect perch for you.",
    "Hoo... another soul at the crossroads.\n\nFear not — I've never led a traveler astray.",
    "You've found Tabiji's roost. Not everyone does.\n\nThat tells me you're ready for something special.",
    "*blinks wisely*\n\nI sense great wanderlust in you. Let's channel it properly.",
    "The journey of a thousand miles begins with one owl.\n\nThat owl is me. Let's get started.",
    "Hoo! Welcome, welcome. Take a seat on this branch.\n\nNow — where does your imagination wander?",
    "I've been watching the migration patterns, and they say... you need a trip.\n\nLet me help with that.",
    "Every traveler who finds me was meant to.\n\nSo tell me — what kind of adventure calls your name?",
    "*tilts head curiously*\n\nHmm, yes. I can see it. You're overdue for a journey.",
    "The maps are spread, the compass is ready.\n\nAll I need is your heart's desire, traveler.",
    "Hoo... the moon told me you'd come seeking wisdom.\n\nLet us find where your feet wish to wander.",
    "Welcome, brave one. I am Tabiji, navigator of dreams.\n\nTogether we'll find your perfect escape.",
    "Ah, fresh wanderlust! I can smell it from here.\n\nSit, rest your wings, and tell me everything.",
    "*perks up*\n\nA visitor! Perfect timing — I just finished studying the atlas.",
    "The forest whispers that a journey awaits you.\n\nLet old Tabiji help you find which one.",
    "Hoo-hoo! You look like someone who needs a change of scenery.\n\nAm I right? Of course I am. I'm an owl.",
    "In all my years of guiding travelers, the excited ones are my favorite.\n\nAnd you look very excited indeed.",
    "Welcome to the edge of the map.\n\nBeyond here, only I know the way. Shall we venture forth?",
    "*fluffs chest feathers proudly*\n\nI have guided poets, explorers, and dreamers. Today, I guide you.",
    "Hoo... every great story starts with a single question.\n\nLet me ask you mine, and your story shall unfold.",
    "The northern winds bring you to me, and the southern winds shall carry you onward.\n\nBut first — a few questions.",
    "I've perched atop every mountain, sailed every sea in spirit.\n\nNow let me lend that wisdom to you.",
    "A new traveler! The branch gets livelier.\n\nTell me what you seek — gold, glory, or perhaps just good food?",
    "Hoo... I see you carry a map, but it's blank.\n\nLet me help you fill it in.",
    "*clicks beak thoughtfully*\n\nYes, yes... I already have some ideas for you. But first, questions.",
    "The owl sees all, knows all, recommends all.\n\nWell, mostly travel. I'm very specialized. Let's begin!",
    "Greetings! I am Tabiji, the wisest travel owl in the land.\n\nModest too. Now — let's find your adventure.",
    "The atlas trembles with anticipation.\n\nA new journey is about to be written. Yours.",
    "Hoo... come, sit beneath the starlight with me.\n\nTell me where your daydreams take you.",
    "Welcome to the crossroads of possibility.\n\nI'll be your guide — feathered, wise, and slightly mysterious.",
    "*yawns, then snaps to attention*\n\nOh! A traveler! Wonderful. I was just meditating on... geography. Yes. Let's begin."
];

const VIBE_QUESTIONS = [
    "What calls to you when you dream of distant lands?",
    "When you close your eyes and imagine travel, what do you see?",
    "What's the first thing that excites you about a new place?",
    "Which of these speaks to your wandering soul?",
    "What flavor of adventure sets your spirit alight?",
    "Picture your perfect day abroad. What's the vibe?",
    "The compass has four points. Which direction pulls you?",
    "What kind of memories do you want to collect?",
    "If travel were a meal, what flavor would you crave?",
    "What makes your heart beat faster when you think of exploring?",
    "The world offers many gifts. Which do you reach for first?",
    "What's the thread that connects your best travel memories?",
    "When wanderlust strikes, what exactly is it calling you toward?",
    "Imagine stepping off a plane. What do you hope to feel?",
    "Which of these would make you drop everything and book a flight?",
    "What's the core of your ideal journey?",
    "The owl asks: what stirs your traveler's heart most deeply?",
    "Tell me — what's the essence of your perfect trip?",
    "Which of these would you tattoo on your suitcase?",
    "What does travel mean to you at its core?",
    "Close your eyes. You're in the perfect place. What surrounds you?",
    "Which energy do you want your next trip to radiate?",
    "The wind carries four scents. Which one do you follow?",
    "What's the feeling you're chasing on your next adventure?",
    "If your ideal destination were a song, what genre would it be?",
    "What pulls you off the couch and onto a plane?",
    "The owl sees many paths. Which type calls to you?",
    "When you scroll travel photos, which ones stop your thumb?",
    "What would make this trip unforgettable for you?",
    "Which of these describes your travel soul?",
    "The feathers detect your energy. But tell me in your own words...",
    "What's the one thing a destination MUST have for you?",
    "Think of your happiest trip memory. What was the dominant vibe?",
    "What do you want your next destination to make you feel?",
    "If you could teleport anywhere right now, what kind of place would it be?",
    "The map unfolds before you. What catches your eye first?",
    "Which of these would you write on your boarding pass?",
    "Your ideal trip revolves around which of these?",
    "What do you want to come home talking about?",
    "The ancient owl wisdom says: choose your essence...",
    "What type of journey does your soul need right now?",
    "When friends ask about your dream trip, you describe...",
    "Which word best describes your ideal destination's personality?",
    "The stars align differently for each traveler. Yours point toward...",
    "What's the heartbeat of your perfect vacation?",
    "If you had one week and unlimited possibility, you'd seek...",
    "Which of these would complete the sentence: 'I travel for...'?",
    "The owl's first question is always the most important. So: what moves you?",
    "Your passport is empty. What kind of stamps do you want to fill it with?",
    "Tabiji peers into your soul and asks: what is it you truly seek?"
];

const ENERGY_QUESTIONS = [
    "When the sun rises, how does your spirit wish to move?",
    "How do you like to spend your days when traveling?",
    "What's your travel speed? Hummingbird or sloth?",
    "When exploring a new city, what's your pace?",
    "The owl observes your energy. Are you a sprinter or a drifter?",
    "How packed do you want your itinerary to be?",
    "Do you travel to DO things, or to simply BE somewhere?",
    "What's your ideal ratio of activity to relaxation?",
    "When you travel, do you collapse into bed at night or stay up for more?",
    "How many things do you want to check off each day?",
    "The owl asks about your rhythm. Fast, steady, or slow?",
    "Picture your ideal travel day. How much are you moving?",
    "Are you the first one up at sunrise, or sleeping till brunch?",
    "How much structure does your perfect day have?",
    "What sounds more like you: '10 things before lunch' or 'one perfect afternoon'?",
    "Do you pack running shoes or a hammock?",
    "The wind blows at different speeds. Which matches yours?",
    "How much energy do you want to pour into this trip?",
    "Are you a 'see everything' traveler or a 'soak it in' traveler?",
    "What's your ideal morning abroad?",
    "The owl watches how travelers move. How do you move?",
    "Would your friends describe your travel style as intense or chill?",
    "How tired do you want to be at the end of each day?",
    "Do you return from trips recharged or gloriously exhausted?",
    "What's your default mode when exploring somewhere new?",
    "The compass needle vibrates at your energy. How fast does it spin?",
    "Do you over-plan or under-plan? Be honest.",
    "How many tabs do you open when researching a trip?",
    "What's your relationship with itineraries?",
    "When traveling, are you an early bird or a night owl?",
    "The wise owl must know: are you all gas or all brakes?",
    "How much wandering vs. planning defines your travel?",
    "What's your ideal balance between adventure and rest?",
    "Do you want to come home needing a vacation from your vacation?",
    "How many hours a day do you like to be 'doing stuff'?",
    "Would you rather see one thing deeply or ten things quickly?",
    "The ancient wisdom asks: do you travel to rest or to conquer?",
    "What pace lets you enjoy a destination most?",
    "Are you a meanderer or a maximizer?",
    "How does your body like to travel?",
    "What's your vacation gear: hiking boots or flip flops?",
    "Do you pre-book everything or figure it out when you arrive?",
    "The owl can tell a lot by how a traveler walks. How do you walk?",
    "Are you here to check boxes or fill your cup?",
    "What's your travel battery like? Energizer bunny or zen monk?",
    "How many steps are on your ideal travel day?",
    "What sounds more relaxing: a full schedule or an empty one?",
    "Do you travel with a highlighter or a hammock?",
    "The feathers ask: does your spirit sprint, stroll, or float?",
    "Tell the owl honestly — how much do you actually want to DO?"
];

const BUDGET_QUESTIONS = [
    "What resources do you bring for this journey?",
    "Let's talk treasure. How much gold are you carrying?",
    "The practical question: what's your travel budget like?",
    "How much are you looking to invest in this adventure?",
    "What's your wallet whispering to you about this trip?",
    "The owl must ask about earthly matters. Your budget?",
    "How deep are the pockets on this journey?",
    "Let's talk coins. Where do you fall?",
    "What level of comfort does your wallet allow?",
    "The practical owl asks: what's the spending vibe?",
    "How fancy are we talking here?",
    "Be honest with old Tabiji — what's the budget situation?",
    "Money question! Every owl asks it. Don't be shy.",
    "How much treasure have you set aside for this quest?",
    "The wind doesn't care about money, but hotels do. Your budget?",
    "What's your ideal spend-per-day mindset?",
    "Are we talking street food or Michelin stars?",
    "Hostels, hotels, or honeymoon suites? Give me a ballpark.",
    "The owl's second-wisest advice: be honest about your budget.",
    "How much do you want to splurge on this trip?",
    "What does 'worth it' look like to you, money-wise?",
    "The coins in your pouch — many, some, or overflowing?",
    "What tier of adventure fits your finances right now?",
    "Budget talk! Promise I won't judge. Much.",
    "How would you describe your travel spending style?",
    "Are you counting coins or swiping without looking?",
    "What's your comfort level on the spending spectrum?",
    "The owl sees three paths: thrifty, balanced, and luxurious. Which?",
    "Your wallet has feelings too. What's it comfortable with?",
    "How much financial fuel are you loading for this trip?",
    "Champagne taste or beer budget? Or somewhere in between?",
    "What matters more: saving money or spending on experiences?",
    "The maps show routes at every price point. Where do you land?",
    "Let's calibrate expectations. What's the budget zone?",
    "How much do you typically budget per day when traveling?",
    "The owl asks without judgment: what are you working with?",
    "Financial reality check — where are we at?",
    "What's your travel spending personality?",
    "Backpacker, mid-range, or bougie? All valid answers.",
    "How much are you willing to invest in memories?",
    "The wise owl says: a trip's value isn't its cost. But still — budget?",
    "Are we stretching pennies or letting loose?",
    "What spending bracket makes you feel comfortable traveling?",
    "Tell Tabiji about your treasure chest situation.",
    "How much gold per night are we looking at?",
    "The feathers detect... let me guess your budget. Or you could just tell me.",
    "What's the financial vibe for this journey?",
    "Your piggy bank says it's time to talk numbers.",
    "How much do you want to allocate to this adventure?",
    "The owl knows money doesn't buy happiness. But it does buy flights. Budget?"
];

const DURATION_QUESTIONS = [
    "How much time can you dedicate to this voyage?",
    "How many days can you escape for?",
    "How long is this adventure going to be?",
    "What's the length of your escape from reality?",
    "Time is the traveler's most precious resource. How much do you have?",
    "How many sunrises will you see abroad?",
    "The calendar asks: how long can you disappear?",
    "What's the time window for this journey?",
    "How much time has the universe granted you for travel?",
    "Quick trip or proper expedition?",
    "How many days until the real world needs you back?",
    "The owl asks about time — the one thing even I can't control.",
    "How long do you want to be 'out of office'?",
    "What's the trip duration that makes your heart sing?",
    "Weekend warrior or extended explorer?",
    "How long until your plants start to worry?",
    "What chunk of time are you carving out for adventure?",
    "How many days before you start missing your bed?",
    "The compass of time points to how many days?",
    "What's the ideal trip length for your soul right now?",
    "How long can you leave your responsibilities behind?",
    "Short and sweet, or long and deep?",
    "How much time are you gifting yourself for this trip?",
    "What's the window of freedom you're working with?",
    "How many chapters long is this travel story?",
    "The owl calculates your available days. How many?",
    "Quick getaway or full-blown adventure?",
    "How long until someone starts asking where you are?",
    "What timeframe does your dream trip need?",
    "How many nights away from home sounds perfect?",
    "The ancient wisdom says: some trips need days, others need weeks. Yours?",
    "How long do you want to lose yourself out there?",
    "What's your out-of-office window looking like?",
    "How many days do you need to truly unwind?",
    "Quick recharge or complete reset?",
    "The migration can be short or long. How far are you flying?",
    "How much calendar space have you cleared for this?",
    "What's the duration that lets you fully decompress?",
    "How long can your email go unanswered?",
    "The owl asks: how many moons will you travel?",
    "What length of trip are you realistically planning?",
    "How long before you need to be back at your perch?",
    "Short hop or long haul? Both have their magic.",
    "How many days of adventure are we planning?",
    "What's your ideal trip length — be greedy!",
    "How long do you want this dream to last?",
    "The feathers sense... tell me how much time you have.",
    "How many days can you steal away from the ordinary?",
    "What's the sweet spot for trip duration, for you?",
    "The owl needs to know: brief escape or epic voyage?"
];

const PRIORITY_QUESTIONS = [
    "If you could carry only one memory home, what would it be?",
    "What's the ONE thing that would make this trip legendary?",
    "When you look back on this trip years later, what do you hope to remember?",
    "What single experience would make the whole trip worth it?",
    "The owl asks the final question: what matters most to you?",
    "If the trip could give you one perfect moment, what would it look like?",
    "What's the non-negotiable for your ideal trip?",
    "Close your eyes. Your trip highlight reel plays. What scene stands out?",
    "What would you tell friends was the BEST part?",
    "The last question reveals the most. What do you value above all?",
    "If you could bottle one moment from this trip, what would it contain?",
    "What's the thing that separates a good trip from an AMAZING one?",
    "Picture your photo album from this trip. What's the hero shot?",
    "What experience would make you immediately start planning a return trip?",
    "The deepest question: what does your soul actually need from this journey?",
    "What would make you say 'that trip changed me'?",
    "If this trip had a highlight, what would it be?",
    "What's the moment you'd replay in your mind forever?",
    "The owl peers deep. What do you truly seek from travel?",
    "What single thing would make you recommend this trip to everyone?",
    "What experience matters most to your traveler's heart?",
    "If the trip were a story, what would the climax be?",
    "What's your 'I can't believe I did that' moment look like?",
    "The wise owl's final wisdom begins with knowing what you treasure most...",
    "What do you want to bring home in your heart?",
    "Picture the moment you'll never forget. What is it?",
    "What would make this trip feel truly complete?",
    "The owl always saves the best question for last. Here it is...",
    "What's the ultimate travel experience for you?",
    "If the trip could deliver one perfect thing, what would you choose?",
    "What's the crown jewel of any great trip, in your eyes?",
    "The final feather falls. Tell me: what do you value most?",
    "What single experience is worth traveling across the world for?",
    "What's the thing that turns a trip into a transformation?",
    "Your last answer reveals your truest self. What matters most?",
    "The owl sees your journey nearing its beginning. One last question...",
    "What memory do you want etched into your soul?",
    "If you could guarantee one thing about this trip, what would it be?",
    "What do you daydream about when you think of the perfect trip?",
    "The winds carry one final question: what is your deepest travel wish?",
    "What would you regret NOT doing on this trip?",
    "What experience do you always come back to when remembering past travels?",
    "The owl tilts its head for the final time. What matters most to you?",
    "What's the one thing that makes you feel truly alive when traveling?",
    "If a genie granted one travel wish, what would it be?",
    "What does the perfect trip look like in its finest moment?",
    "The last piece of the puzzle: what do you hold dearest?",
    "What kind of moment are you chasing?",
    "What would make you shed a tear of joy on this trip?",
    "Final question, traveler. Make it count: what do you care about most?"
];

// Response pools for each choice
const RESPONSES = {
    // Vibe responses
    adventure: [
        "A bold spirit. The mountains call to those who dare.",
        "The wild beckons! I like your courage, traveler.",
        "Adrenaline seeker! The world has peaks and rapids waiting for you.",
        "Adventure! The owl approves. Fortune favors the brave.",
        "Hoo! A thrill-chaser! I know just the winds to send you on.",
        "The untamed path — yes, I see fire in your eyes.",
        "Risk and reward, summit and valley. You seek the full spectrum.",
        "Bold choice. The greatest stories start with 'I went for it.'",
        "*feathers ruffle with excitement* Adventure it is!",
        "You want to feel ALIVE out there. I respect that enormously."
    ],
    culture: [
        "Wisdom seeks wisdom. You wish to learn from ages past.",
        "A kindred spirit! History has so much to teach the willing student.",
        "The old stones have stories. You're wise enough to listen.",
        "Culture! The deepest way to understand a place. Well chosen.",
        "Museums, temples, traditions — the owl's own favorite pursuits.",
        "You travel to understand, not just to see. That takes depth.",
        "Hoo... a lover of heritage. The ancient walls will welcome you.",
        "History and tradition — the roots that give travel its meaning.",
        "A scholar's heart in a traveler's body. Rare and wonderful.",
        "You seek the soul of a place. That's the wisest journey of all."
    ],
    foodie: [
        "The belly is the gateway to understanding a people.",
        "A food pilgrim! The greatest adventures happen at the table.",
        "You speak my language. Every culture reveals itself through its cuisine.",
        "Hoo-hoo! A traveler who eats with purpose. The best kind!",
        "The spice route of the soul! Food connects us all.",
        "Markets, street stalls, hidden restaurants — your treasure map is a menu.",
        "You travel for flavors. The owl deeply, deeply respects this.",
        "They say you can taste a culture's heart. You already know this.",
        "The stomach leads where the heart follows. Wise, very wise.",
        "Food is memory, food is love, food is culture. You understand."
    ],
    relaxation: [
        "Stillness is its own kind of journey.",
        "Peace. The most underrated adventure of all.",
        "The owl knows: sometimes the bravest thing is to simply rest.",
        "Restoration! The world is loud. You need somewhere quiet.",
        "A calm soul seeks calm waters. I know just the places.",
        "Hoo... you need to breathe. Let me find you somewhere perfect.",
        "Rest is not laziness — it's wisdom. The owl approves.",
        "The gentlest journeys leave the deepest impressions.",
        "You seek sanctuary. The world has beautiful ones hidden everywhere.",
        "Sometimes the greatest adventure is doing absolutely nothing, perfectly."
    ],
    // Energy responses
    high: [
        "Your flame burns bright. We need a place to match your fire.",
        "Maximum energy! I'll find you somewhere that can keep up.",
        "You want to see EVERYTHING. The owl loves this energy!",
        "High octane! Clear your camera roll — you'll need the space.",
        "A true explorer! Dawn to midnight, every moment counts.",
        "Hoo! Your enthusiasm could power a small city!",
        "The energizer traveler! I'll make sure every hour is packed.",
        "All gas, no brakes! I respect the commitment.",
        "You'll sleep on the plane home. While there — ADVENTURE!",
        "That's the spirit! Let's fill every second with something amazing."
    ],
    medium: [
        "Movement and rest in harmony, like day and night.",
        "The balanced path. Activity and leisure in perfect rhythm.",
        "Smart — you know that the best trips have breathing room.",
        "A morning adventure, an afternoon café. You've figured out travel.",
        "Balance! The owl's favorite word. Besides 'mice.'",
        "Steady and sustainable. You'll enjoy every moment without burning out.",
        "The middle way — the wisest travelers always find it.",
        "Enough energy to explore, enough space to savor. Perfect.",
        "You want the best of both worlds. I can work with that.",
        "A traveler who knows their rhythm. That's true self-awareness."
    ],
    low: [
        "Not all journeys are measured in steps.",
        "Gentle wandering. The owl approves of this peaceful approach.",
        "You travel to rest, and that's perfectly beautiful.",
        "Slow travel is deep travel. You'll see things others miss.",
        "The unhurried path reveals the most hidden treasures.",
        "Recharge mode — activated. Let me find your sanctuary.",
        "Sometimes the best view is from a hammock. I respect that.",
        "Quality over quantity. One perfect moment beats ten rushed ones.",
        "The slow traveler sees what the fast one blurs past.",
        "Peace and presence. Your trip will be a meditation."
    ],
    // Budget responses
    budget_low: [
        "The simplest paths often reveal the greatest treasures.",
        "Budget travel is an art, and you're about to make a masterpiece.",
        "The owl knows: the best things in life are free. Or cheap.",
        "Street food, local buses, hidden gems. That's the REAL travel.",
        "More money doesn't mean more magic. Sometimes it's the opposite.",
        "Thrifty and adventurous — the world's best combination!",
        "Budget travelers see the real side of every destination.",
        "The most memorable meals often cost the least. True story.",
        "Hoo! Traveling light on the wallet? I know incredible spots for you.",
        "Smart spending, rich experiences. The owl's own philosophy."
    ],
    budget_mid: [
        "Balance in all things. You understand the owl's way.",
        "A comfortable middle — enough for joy without the stress.",
        "Smart spending with room for treats. The sweet spot!",
        "Neither too much nor too little. You travel wisely.",
        "The golden middle path. Comfort without excess.",
        "Practical but not stingy. Generous but not wasteful. Perfect.",
        "You know when to save and when to splurge. That's talent.",
        "Moderate and mindful. Every dollar will go to good use.",
        "The middle way strikes again! The owl is a fan.",
        "Balanced budget, balanced trip. The equation works out beautifully."
    ],
    budget_high: [
        "I shall find you something worthy of your investment.",
        "No limits? Oh, the places I can send you!",
        "Luxury! The owl rarely gets to recommend the finest perches.",
        "Top shelf it is. Prepare for something extraordinary.",
        "When you invest in travel, travel invests in you. Generously.",
        "Splendid! I'll pull from the premium collection.",
        "The finest experiences await those willing to invest. Lucky you!",
        "Hoo-hoo! The VIP treatment! I have special recommendations.",
        "Money well spent on travel is never wasted. The owl guarantees it.",
        "Luxury traveler! Let me open the vault of extraordinary destinations."
    ],
    // Duration responses
    weekend: [
        "Brief but meaningful. Every moment will count.",
        "A quick escape! Short trips can hold infinite magic.",
        "Three to four days — enough for a great reset.",
        "Short and sweet. I'll make sure every hour matters.",
        "The perfect long weekend can change everything. Truly.",
        "Quick getaway! Sometimes that's all you need to feel alive.",
        "Brief trips demand great destinations. Good thing I know them.",
        "A sprint of joy! Let me maximize your short window.",
        "Even a few days somewhere new can shift your whole perspective.",
        "Hoo! A quick escape. I'll make it count double."
    ],
    week: [
        "Time enough to truly arrive, not just visit.",
        "A full week — now we're talking! Room to explore properly.",
        "Seven days is the sweet spot. Enough to really know a place.",
        "A week! The perfect canvas for a great trip.",
        "With a week, you'll stop being a tourist and start being a traveler.",
        "Seven sunrises, seven sunsets, infinite possibilities.",
        "A proper week lets you find the hidden spots. I love it.",
        "The owl recommends a week minimum for most destinations. Smart choice!",
        "With seven days, we can craft something truly special.",
        "A week of freedom! Let me fill it with wonder."
    ],
    extended: [
        "A true journey. You seek transformation, not just travel.",
        "Two weeks or more! Now THAT is a proper adventure.",
        "Extended travel — the only way to truly understand a place.",
        "Hoo! You're giving yourself the gift of time. The wisest choice.",
        "Long trips reveal what short trips only hint at.",
        "Two weeks plus? The deep cuts, the hidden gems, the REAL stories.",
        "This isn't a vacation — this is an expedition. I love it!",
        "With this much time, you won't just visit. You'll belong.",
        "Extended adventures let you follow the unexpected paths. The best ones.",
        "The owl reserves its finest recommendations for long-haul travelers."
    ],
    // Priority responses
    food: [
        "Taste is memory made physical.",
        "The meal that changes your life is waiting somewhere. Let's find it.",
        "A true food pilgrim! The greatest memories are often edible.",
        "The belly remembers what the mind forgets. Wise priority.",
        "Hoo! Food as the centerpiece. The owl couldn't agree more.",
        "One perfect meal can define an entire trip. You know this.",
        "Flavor is the fastest portal to another culture. Well chosen.",
        "The dish you'll dream about for years — let's go find it.",
        "Food is love in edible form. Your trip will be delicious.",
        "A culinary quest! The most noble of all travel priorities."
    ],
    nature: [
        "Nature speaks to those who listen.",
        "The world's beauty needs no museum. It's already on display.",
        "A breathtaking vista — the kind that makes you forget to breathe.",
        "Nature is the greatest artist. You seek her masterpiece.",
        "Hoo... landscapes that stop you mid-step. I know those places.",
        "The view that changes your wallpaper AND your perspective.",
        "Mountains, oceans, forests — the original wonders. Good taste!",
        "You seek the jaw-drop moment. I know exactly where to find it.",
        "Nature's beauty heals things you didn't know were broken.",
        "The owls' world is nature's world. I'll guide you to the finest."
    ],
    local: [
        "The greatest journeys are measured in friendships.",
        "Connection! The beating heart of meaningful travel.",
        "Real conversations with real people — the ultimate souvenir.",
        "You want the authentic experience. Not the tourist version. Respect.",
        "Meeting locals transforms you from visitor to guest. Beautiful.",
        "The human connection — no guidebook can replicate it.",
        "Hoo! A people person! The warmest travels await you.",
        "Local connections reveal the secret layer of every destination.",
        "The stories you'll hear from locals will outshine any monument.",
        "Travel is ultimately about human connection. You understand this deeply."
    ],
    photos: [
        "To capture a moment is to honor it.",
        "The perfect shot — where the light, place, and moment align.",
        "A photographer's eye! You see beauty others walk right past.",
        "That one photo that makes everyone ask 'WHERE is that?!'",
        "Hoo! A visual storyteller! I know the most photogenic spots.",
        "The picture that makes time stand still. Let's find yours.",
        "Some moments are so beautiful, you MUST capture them.",
        "Instagram-worthy doesn't even begin to cover what I have in mind.",
        "The photo you frame and hang on your wall forever. That's the goal.",
        "You seek visual magic. The world has plenty — let me show you."
    ]
};

const SURPRISE_TEXTS = [
    "The winds have chosen for you! Let me see what fate has in store...",
    "Leaving it to fate? Bold move! The owl loves a gambler.",
    "Surprise me? Oh, I DO love when travelers trust the wind!",
    "Random it is! Sometimes the universe knows better than we do.",
    "*spins the globe dramatically* Where it stops, nobody knows!",
    "Letting destiny decide! The bravest choice of all.",
    "Hoo-hoo! A leap of faith! Let the stars decide your path!",
    "You trust old Tabiji? I'm honored. Let me weave something special.",
    "The dice are cast! Adventure awaits wherever they land!",
    "Spontaneity! The secret ingredient of the best trips.",
    "No plan IS the plan! The owl scrambles the feathers...",
    "*closes eyes, feels the wind* Ah yes... I see your path forming...",
    "Rolling the cosmic dice! Fortune favors the spontaneous!",
    "You want the full mystery? I'll conjure something wild!",
    "The randomness of the universe has never disappointed. Let's go!",
    "Trust the owl, trust the wind, trust the adventure!",
    "A surprise journey! These are always the ones you remember most.",
    "*flaps wings excitedly* Oh this is going to be GOOD!",
    "The universe conspires for those who surrender to it. Let's see...",
    "Leaving it to chance? The owl's heart soars!",
    "The map spins, the compass whirls... and your destiny emerges!",
    "Chaos is just adventure without a plan! Here we go!",
    "You want me to surprise you? Oh, you have NO idea what I have in store.",
    "Fate, meet traveler. Traveler, meet fate. You two will get along.",
    "The winds are swirling! Something wonderful is taking shape...",
    "Random? There's nothing random about it. The universe KNOWS.",
    "Surprise! Plot twist! Adventure! Let me work my magic!",
    "*ruffles every feather* Oh, the excitement! Calculating your destiny...",
    "You just handed me creative freedom. The owl is THRILLED.",
    "Some call it random. I call it destiny. Let's find yours!",
    "The spontaneous path is the one that leads to the best stories.",
    "No preferences? No problem! The owl sees ALL paths!",
    "Trust the process! The feathers are aligning...",
    "Adventure through chaos! The most beautiful kind!",
    "The void of indecision becomes the canvas of possibility!",
    "Picking for you? My FAVORITE thing to do!",
    "*adjusts spectacles dramatically* Stand back. Owl magic at work.",
    "The elements converge... your surprise destination awaits!",
    "Going full random? The owl literally lives for this!",
    "No compass needed — pure instinct from here. I love it!",
    "The cosmic owl-gorithm is processing... beep boop hoo!",
    "Let go of control and grab onto wonder! Here we go!",
    "Tabiji's Wild Card! These always produce the best results.",
    "You want chaos? I'll give you BEAUTIFUL chaos!",
    "The feathers are falling where they may... and they're falling perfectly.",
    "Random path selected! Plot twist energy: maximum!",
    "The universe appreciates your trust. Let me deliver something stellar.",
    "Full surprise mode! Engaging owl turbines...",
    "A traveler who trusts fate is a traveler after my own heart!",
    "No choices needed — the wind already knows where you should go!"
];

const RESULT_REVEAL_TEXTS = [
    "The winds whisper to me...\n\n*ruffles feathers*\n\nYes. I see your path.",
    "The feathers are aligning...\n\n*peers into the distance*\n\nAh, yes. It's clear now.",
    "*closes eyes*\n\nThe ancient maps are revealing your destiny...\n\nI see it!",
    "Hmm... hmmm...\n\n*taps talon thoughtfully*\n\nYES! I know exactly where you belong.",
    "The compass spins... and settles.\n\n*nods wisely*\n\nYour path is revealed.",
    "*fluffs feathers dramatically*\n\nThe stars have spoken.\n\nI have your answer.",
    "Let me consult the winds...\n\n*listens intently*\n\nThey've never been so certain.",
    "Processing owl-gorithm...\n\n*blinks mysteriously*\n\nDestination: confirmed.",
    "The migration patterns converge...\n\n*gasps*\n\nThis is going to be perfect.",
    "*stares into the sunset*\n\nI see mountains... or beaches... or both.\n\nYes. I have it.",
    "The ancient knowledge flows through me...\n\n*vibrates slightly*\n\nYour journey crystallizes!",
    "Calculating... meditating... owl-culating...\n\n*beams*\n\nGot it!",
    "The threads of your answers weave together...\n\n*admires the tapestry*\n\nBeautiful.",
    "*closes one eye, then the other*\n\nThe owl's eye sees true.\n\nHere is your path.",
    "Somewhere on this earth, a place awaits you specifically.\n\n*points with wing*\n\nFound it.",
    "The wind, the stars, and your own heart agree...\n\n*nods solemnly*\n\nI see clearly.",
    "Cross-referencing owl databases...\n\n*feathers compute*\n\nResults incoming!",
    "The tea leaves — well, mouse bones actually — they don't lie.\n\nI see your path!",
    "*spins on branch*\n\nThe world speaks!\n\nAnd it says THIS is where you should go.",
    "Every answer you gave was a breadcrumb. And I've followed the trail.\n\nLook where it leads!",
    "The owl oracle awakens...\n\n*glows mysteriously*\n\nI have your destinations.",
    "Hmm, let me check my extensive travel database...\n\n*taps head*\n\nPerfect match found!",
    "The cosmic algorithm has rendered its verdict.\n\n*stamps with talon*\n\nSo it is written!",
    "*peers through ancient monocle*\n\nThe map reveals itself.\n\nYour journey awaits.",
    "After much deliberation with the winds...\n\n*nods approvingly*\n\nI have just the thing.",
    "The stars whisper their recommendation...\n\nAnd who am I to argue with stars?",
    "*meditates briefly*\n\n...hoo.\n\n...HOO!\n\nYES! I've found your perfect match!",
    "The feather-compass has settled.\n\n*looks up triumphantly*\n\nBehold your destiny!",
    "Consulting the Tabiji archives...\n\nVolume 47... section 12...\n\nAHA! Here it is!",
    "Your answers paint a picture. And I recognize this picture.\n\nI know exactly where you need to go.",
    "*dramatic pause*\n\n...\n\n*longer pause*\n\nOkay I actually had the answer immediately. Here!",
    "The owl has deliberated.\n\nThe owl has decided.\n\nThe owl is quite pleased with itself.",
    "Running ancient algorithms...\n\nJust kidding, I'm an owl. But I DO know travel.\n\nHere!",
    "The puzzle pieces fall into place...\n\n*click, click, click*\n\nCompleted!",
    "My feathers stood up at your answers. That's a VERY good sign.\n\nLook what I found!",
    "The wind patterns, your energy, the stars — they all converge here.\n\nRemarkable.",
    "*excitedly hopping on branch*\n\nOh this is a GREAT match! I'm genuinely excited for you!",
    "Destiny computation: complete.\n\nSatisfaction prediction: very high.\n\nHere we go!",
    "The ancient owl GPS has locked on.\n\n*recalculating... recalculating...*\n\nRoute found!",
    "Your soul's coordinates have been triangulated.\n\n*adjusts spectacles*\n\nRemarkable precision.",
    "I've matched exactly 0.014% of my knowledge to your answers.\n\nThat's the GOOD 0.014%.",
    "The migratory instinct kicks in...\n\n*feels the pull*\n\nI know where you must fly.",
    "Results are in. And honestly?\n\n*chef's kiss*\n\nThis is some of my finest work.",
    "The prophecy unfolds...\n\nWell, it's more of a recommendation. But 'prophecy' sounds better.",
    "If I had eyebrows, they'd be raised. What a great set of answers.\n\nHere's what I found!",
    "The universe has spoken through the medium of quiz answers.\n\nAnd it said THIS:",
    "*vibrating with excitement*\n\nOh you are going to LOVE this recommendation!",
    "My ancient wisdom + your modern wanderlust = one incredible destination.\n\nBehold!",
    "Alert: perfect match detected!\n\n*owl alarms blaring*\n\nI have your results!",
    "After decades of guiding travelers... these are some of my finest picks yet."
];

const RESULT_FOUND_TEXTS = [
    "I have found {n} paths for your journey:",
    "Behold! {n} destinations worthy of your spirit:",
    "The winds reveal {n} perfect matches for your soul:",
    "{n} paths emerge from the mist. All lead to adventure:",
    "My wisdom has uncovered {n} destinations just for you:",
    "The compass points to {n} extraordinary places:",
    "{n} destinations rise from my ancient maps:",
    "The owl has spoken! Here are your {n} destined paths:",
    "Drumroll please... {n} incredible matches found:",
    "From 706 destinations, these {n} call your name the loudest:",
    "{n} perfect fits have revealed themselves:",
    "The stars align at exactly {n} coordinates:",
    "Your answers unlocked {n} hidden destinations:",
    "Tabiji presents: your {n} ideal journeys:",
    "The feather-compass settles on {n} magnificent choices:",
    "{n} paths unfold before you. Each one magical:",
    "The oracle reveals {n} destinations crafted for your spirit:",
    "After much owl contemplation, {n} winners emerge:",
    "I've narrowed the entire world down to {n} perfect spots:",
    "Here they are — {n} destinations that match your soul:",
    "{n} extraordinary matches await your exploration:",
    "The migration map shows {n} ideal landing spots:",
    "Prepare yourself — {n} incredible destinations incoming:",
    "My finest recommendations: {n} paths tailored to you:",
    "The wind carries {n} names to my ear. Let me share them:",
    "{n} destinations that tick every box:",
    "The verdict is in! {n} outstanding matches:",
    "{n} places where you'll feel completely at home:",
    "Tabiji's top {n} picks for YOUR unique journey:",
    "The ancient maps glow at {n} locations. Here they are:",
    "I present to you {n} destinations of destiny:",
    "{n} places that are basically calling your name right now:",
    "The owl's algorithm returns {n} perfect results:",
    "Out of everywhere on Earth, these {n} are YOUR spots:",
    "{n} destinations have earned the Tabiji seal of approval:",
    "Clear your schedule — {n} life-changing trips await:",
    "The cosmic travel agent recommends {n} incredible options:",
    "{n} adventures perfectly calibrated to your preferences:",
    "Your personalized travel destiny: {n} amazing choices:",
    "Feast your eyes on {n} handpicked destinations:",
    "The owl shortlist: {n} destinations you'll absolutely love:",
    "{n} places so perfect for you, it's almost eerie:",
    "Calculating compatibility... {n} destinations at 95%+ match!",
    "I'm particularly proud of these {n} recommendations:",
    "The final reveal: {n} destinations chosen by wind and wisdom:",
    "{n} jewels plucked from the world map, just for you:",
    "My talons point to exactly {n} perfect destinations:",
    "The great reveal! {n} extraordinary matches found:",
    "These {n} destinations didn't just match — they RESONATED:",
    "Presenting your {n} owl-certified, wind-approved destinations:"
];

// Build dialogue flow dynamically with random text
function buildDialogueFlow() {
    return [
        {
            id: 'intro',
            text: pick(INTRO_TEXTS),
            expression: 'neutral',
            nextStep: 'vibe'
        },
        {
            id: 'vibe',
            text: pick(VIBE_QUESTIONS),
            expression: 'thinking',
            choices: [
                { label: "🏔️ Adventure and thrills", value: "adventure", response: pick(RESPONSES.adventure) },
                { label: "🏛️ Culture and history", value: "culture", response: pick(RESPONSES.culture) },
                { label: "🍜 Food and flavors", value: "foodie", response: pick(RESPONSES.foodie) },
                { label: "🌴 Peace and restoration", value: "relaxation", response: pick(RESPONSES.relaxation) }
            ],
            stateKey: 'vibe',
            nextStep: 'energy'
        },
        {
            id: 'energy',
            text: pick(ENERGY_QUESTIONS),
            expression: 'neutral',
            choices: [
                { label: "⚡ Endlessly — see it all", value: "high", response: pick(RESPONSES.high) },
                { label: "☯️ A balanced rhythm", value: "medium", response: pick(RESPONSES.medium) },
                { label: "🌙 Gently — recharge mode", value: "low", response: pick(RESPONSES.low) }
            ],
            stateKey: 'energy',
            nextStep: 'budget'
        },
        {
            id: 'budget',
            text: pick(BUDGET_QUESTIONS),
            expression: 'thinking',
            choices: [
                { label: "🎒 Budget-friendly", value: "low", response: pick(RESPONSES.budget_low) },
                { label: "💼 Comfortable middle", value: "mid", response: pick(RESPONSES.budget_mid) },
                { label: "💎 Ready to splurge", value: "high", response: pick(RESPONSES.budget_high) }
            ],
            stateKey: 'budget',
            nextStep: 'duration'
        },
        {
            id: 'duration',
            text: pick(DURATION_QUESTIONS),
            expression: 'neutral',
            choices: [
                { label: "🚀 Quick escape (3-4 days)", value: "weekend", response: pick(RESPONSES.weekend) },
                { label: "🗓️ A proper week", value: "week", response: pick(RESPONSES.week) },
                { label: "🌍 Extended adventure (2+ weeks)", value: "extended", response: pick(RESPONSES.extended) }
            ],
            stateKey: 'duration',
            nextStep: 'priority'
        },
        {
            id: 'priority',
            text: pick(PRIORITY_QUESTIONS),
            expression: 'neutral',
            choices: [
                { label: "🍽️ An unforgettable meal", value: "food", response: pick(RESPONSES.food) },
                { label: "🏞️ A breathtaking landscape", value: "nature", response: pick(RESPONSES.nature) },
                { label: "🤝 Connection with locals", value: "local", response: pick(RESPONSES.local) },
                { label: "📸 A perfect photograph", value: "photos", response: pick(RESPONSES.photos) }
            ],
            stateKey: 'priority',
            nextStep: 'result'
        }
    ];
}

// Generate fresh dialogue each game
let DIALOGUE_FLOW = buildDialogueFlow();

// Click to skip typing
dialogueBox.addEventListener('click', () => {
    if (state.isTyping) {
        state.skipRequested = true;
    }
});

// Back button handler
backBtn.addEventListener('click', goBack);

// Surprise me handler
surpriseBtn.addEventListener('click', surpriseMe);

// Typing effect with skip support
async function typeText(text, element) {
    state.isTyping = true;
    state.skipRequested = false;
    dialogueBox.classList.add('typing');
    dialogueBox.classList.remove('not-typing');
    skipHint.classList.remove('hidden');
    element.textContent = '';

    for (let i = 0; i < text.length; i++) {
        if (state.skipRequested) {
            element.textContent = text;
            break;
        }
        element.textContent += text[i];
        const delay = text[i] === '\n' ? 30 : text[i] === '.' ? 25 : 12;
        await sleep(delay);
    }

    state.isTyping = false;
    dialogueBox.classList.remove('typing');
    dialogueBox.classList.add('not-typing');
    skipHint.classList.add('hidden');
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Set NPC expression
function setExpression(expression) {
    npcSprite.className = 'npc-image ' + expression;
}

// Update progress indicator
function updateProgress(stepId) {
    const stepIndex = QUESTION_ORDER.indexOf(stepId);
    if (stepIndex === -1) {
        progressArea.style.display = 'none';
        return;
    }

    progressArea.style.display = 'block';
    progressLabel.textContent = `Question ${stepIndex + 1} of ${QUESTION_ORDER.length}`;

    document.querySelectorAll('.progress-dot').forEach((dot, i) => {
        dot.classList.remove('active', 'completed');
        if (i < stepIndex) {
            dot.classList.add('completed');
        } else if (i === stepIndex) {
            dot.classList.add('active');
        }
    });
}

// Update navigation
function updateNav(stepId) {
    const stepIndex = QUESTION_ORDER.indexOf(stepId);
    if (stepIndex === -1) {
        navArea.style.display = 'none';
        return;
    }

    navArea.style.display = 'flex';
    backBtn.disabled = state.history.length === 0;
}

// Go back to previous question
async function goBack() {
    if (state.history.length === 0) return;

    const prevState = state.history.pop();
    state.answers = { ...prevState.answers };
    state.currentStep = prevState.stepIndex;

    choicesArea.innerHTML = '';

    const step = DIALOGUE_FLOW.find(d => d.id === prevState.stepId);
    await runDialogueStep(step);
}

// Surprise me - random answers
async function surpriseMe() {
    // Fill in remaining answers randomly
    QUESTION_ORDER.forEach(key => {
        if (!state.answers[key]) {
            const step = DIALOGUE_FLOW.find(d => d.stateKey === key);
            if (step && step.choices) {
                const randomChoice = step.choices[Math.floor(Math.random() * step.choices.length)];
                state.answers[key] = randomChoice.value;
            }
        }
    });

    choicesArea.innerHTML = '';
    navArea.style.display = 'none';
    progressArea.style.display = 'none';

    setExpression('excited');
    await typeText(pick(SURPRISE_TEXTS), dialogueText);
    await sleep(300);

    showResult();
}

// Render choices
function renderChoices(choices, stateKey, nextStep) {
    choicesArea.innerHTML = '';

    choices.forEach((choice, index) => {
        const btn = document.createElement('button');
        btn.className = 'choice-btn';
        btn.textContent = choice.label;
        btn.addEventListener('click', () => handleChoice(choice, stateKey, nextStep));

        btn.style.opacity = '0';
        btn.style.transform = 'translateX(-20px)';
        choicesArea.appendChild(btn);

        setTimeout(() => {
            btn.style.transition = 'all 0.3s ease';
            btn.style.opacity = '1';
            btn.style.transform = 'translateX(0)';
        }, index * 80);
    });
}

// Handle choice selection
async function handleChoice(choice, stateKey, nextStep) {
    // Save to history before changing
    state.history.push({
        stepId: stateKey,
        stepIndex: state.currentStep,
        answers: { ...state.answers }
    });

    // Save answer
    state.answers[stateKey] = choice.value;
    state.currentStep++;

    // Clear choices
    choicesArea.innerHTML = '';

    // Show response
    setExpression('smug');
    await typeText(choice.response, dialogueText);

    await sleep(300);

    // Progress to next step
    if (nextStep === 'result') {
        navArea.style.display = 'none';
        progressArea.style.display = 'none';
        showResult();
    } else {
        const nextDialogue = DIALOGUE_FLOW.find(d => d.id === nextStep);
        await runDialogueStep(nextDialogue);
    }
}

// Run a dialogue step
async function runDialogueStep(step) {
    updateProgress(step.id);
    updateNav(step.id);
    setExpression(step.expression);
    await typeText(step.text, dialogueText);

    if (step.choices) {
        await sleep(150);
        renderChoices(step.choices, step.stateKey, step.nextStep);
    }
}

// Calculate best destinations (returns top 3)
function findBestDestinations() {
    const { vibe, energy, budget, duration, priority } = state.answers;

    let scored = DESTINATIONS.map(dest => {
        let score = 0;

        // Vibe match (most important)
        if (dest.vibes.includes(vibe)) score += 3;

        // Budget match
        if (dest.budget === budget) score += 2;
        else if ((dest.budget === 'mid' && budget !== 'high') || budget === 'mid') score += 1;

        // Energy → vibe mapping
        if (energy === 'high' && (dest.originalVibes.includes('Adventure') || dest.originalVibes.includes('Nightlife') || dest.originalVibes.includes('City'))) score += 2;
        if (energy === 'low' && (dest.originalVibes.includes('Relaxation') || dest.originalVibes.includes('Beach') || dest.originalVibes.includes('Romantic'))) score += 2;
        if (energy === 'medium') score += 1;

        // Priority bonuses
        if (priority === 'food' && (dest.originalVibes.includes('City') || dest.originalVibes.includes('Cultural'))) score += 2;
        if (priority === 'nature' && (dest.originalVibes.includes('Nature') || dest.originalVibes.includes('Hiking'))) score += 3;
        if (priority === 'local' && (dest.originalVibes.includes('Cultural') || dest.originalVibes.includes('Unfrequented'))) score += 2;
        if (priority === 'photos' && (dest.originalVibes.includes('Nature') || dest.originalVibes.includes('Romantic') || dest.originalVibes.includes('Beach'))) score += 2;

        // Duration bonuses
        if (duration === 'extended' && dest.travel.includes('adventure')) score += 1;
        if (duration === 'weekend' && dest.originalVibes.includes('City')) score += 1;

        // Small random factor to vary results
        score += Math.random() * 0.5;

        return { ...dest, score };
    });

    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, 3);
}

// Build destination card HTML (photo card format)
function buildDestinationCard(dest, index) {
    const isTopPick = index === 0;
    const seasonIcon = dest.season ? '📅' : '';

    return `
        <div class="destination-card ${isTopPick ? 'top-pick' : ''}" data-id="${dest.id}">
            ${isTopPick ? '<div class="card-badge">Top Pick</div>' : ''}
            <div class="card-photo-wrapper">
                <img class="card-photo" src="${dest.photo}" alt="${dest.name}" loading="lazy" onerror="this.style.display='none'">
            </div>
            <div class="card-body">
                <div class="card-destination-name">${dest.name}, ${dest.region}</div>
                <div class="card-continent">${dest.continent}</div>
                <div class="card-tagline">${dest.tagline}</div>
                <div class="card-tags">
                    ${dest.originalVibes.map(v => `<span class="card-tag">${v}</span>`).join('')}
                </div>
                ${dest.season ? `<div class="card-season">${seasonIcon} ${dest.season}</div>` : ''}
                <div class="card-budget">${dest.budgetLabel}</div>
                <a class="plan-trip-btn" href="/plan/?destination=${encodeURIComponent(dest.name + ', ' + dest.region)}" onclick="if(typeof gtag==='function')gtag('event','plan_trip_click',{event_category:'owl_quiz',destination:dest.name})">
                    ✈️ Plan Trip
                </a>
            </div>
        </div>
    `;
}

// Share results
function shareResults() {
    const destinations = findBestDestinations();
    const topPick = destinations[0];

    const shareText = `Tabiji the Wise Travel Owl recommends: ${topPick.name}! "${topPick.tagline}" - Try it yourself at https://tabiji.ai`;

    if (navigator.share) {
        navigator.share({
            title: 'My Travel Recommendation',
            text: shareText
        }).catch(() => {
            copyToClipboard(shareText);
        });
    } else {
        copyToClipboard(shareText);
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!');
    }).catch(() => {
        showToast('Could not copy');
    });
}

function showToast(message) {
    let toast = document.querySelector('.share-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.className = 'share-toast';
        document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 2000);
}

// Show the trip result
async function showResult() {
    setExpression('thinking');
    await typeText(pick(RESULT_REVEAL_TEXTS), dialogueText);

    await sleep(400);

    const destinations = findBestDestinations();

    setExpression('excited');
    await typeText(pick(RESULT_FOUND_TEXTS).replace('{n}', destinations.length), dialogueText);

    await sleep(250);

    // Build result HTML
    const resultHTML = `
        <div class="trip-header">
            YOUR DESTINED PATHS
        </div>

        <div class="destinations-grid">
            ${destinations.map((dest, i) => buildDestinationCard(dest, i)).join('')}
        </div>

        <div class="result-actions">
            <button class="share-btn" onclick="shareResults()">
                Share Results
            </button>
            <button class="restart-btn" onclick="restart()">
                Seek New Path
            </button>
        </div>
    `;

    tripResult.innerHTML = resultHTML;
    tripResult.style.display = 'block';
    tripResult.style.opacity = '0';

    await sleep(100);
    tripResult.style.transition = 'opacity 0.5s ease';
    tripResult.style.opacity = '1';
}

// Restart the game
function restart() {
    state.answers = {
        vibe: null,
        energy: null,
        budget: null,
        duration: null,
        priority: null
    };
    state.history = [];
    state.currentStep = 0;

    // Regenerate dialogue with fresh random text
    DIALOGUE_FLOW = buildDialogueFlow();

    tripResult.style.display = 'none';
    tripResult.innerHTML = '';

    startGame();
}

// Start the game
async function startGame() {
    setExpression('neutral');
    const intro = DIALOGUE_FLOW.find(d => d.id === 'intro');
    await runDialogueStep(intro);

    await sleep(400);

    const firstQuestion = DIALOGUE_FLOW.find(d => d.id === 'vibe');
    await runDialogueStep(firstQuestion);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    startGame();
});
