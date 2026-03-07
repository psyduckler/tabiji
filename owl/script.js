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

// Dialogue flow - Tabiji's wise personality
const DIALOGUE_FLOW = [
    {
        id: 'intro',
        text: "Hoo... welcome, traveler. I am Tabiji.\n\nTell me your heart's yearning, and I shall reveal your path.",
        expression: 'neutral',
        nextStep: 'vibe'
    },
    {
        id: 'vibe',
        text: "What calls to you when you dream of distant lands?",
        expression: 'thinking',
        choices: [
            { label: "🏔️ Adventure and thrills", value: "adventure", response: "A bold spirit. The mountains call to those who dare." },
            { label: "🏛️ Culture and history", value: "culture", response: "Wisdom seeks wisdom. You wish to learn from ages past." },
            { label: "🍜 Food and flavors", value: "foodie", response: "The belly is the gateway to understanding a people." },
            { label: "🌴 Peace and restoration", value: "relaxation", response: "Stillness is its own kind of journey." }
        ],
        stateKey: 'vibe',
        nextStep: 'energy'
    },
    {
        id: 'energy',
        text: "When the sun rises, how does your spirit wish to move?",
        expression: 'neutral',
        choices: [
            { label: "⚡ Endlessly — see it all", value: "high", response: "Your flame burns bright. We need a place to match your fire." },
            { label: "☯️ A balanced rhythm", value: "medium", response: "Movement and rest in harmony, like day and night." },
            { label: "🌙 Gently — recharge mode", value: "low", response: "Not all journeys are measured in steps." }
        ],
        stateKey: 'energy',
        nextStep: 'budget'
    },
    {
        id: 'budget',
        text: "What resources do you bring for this journey?",
        expression: 'thinking',
        choices: [
            { label: "🎒 Budget-friendly", value: "low", response: "The simplest paths often reveal the greatest treasures." },
            { label: "💼 Comfortable middle", value: "mid", response: "Balance in all things. You understand the owl's way." },
            { label: "💎 Ready to splurge", value: "high", response: "I shall find you something worthy of your investment." }
        ],
        stateKey: 'budget',
        nextStep: 'duration'
    },
    {
        id: 'duration',
        text: "How much time can you dedicate to this voyage?",
        expression: 'neutral',
        choices: [
            { label: "🚀 Quick escape (3-4 days)", value: "weekend", response: "Brief but meaningful. Every moment will count." },
            { label: "🗓️ A proper week", value: "week", response: "Time enough to truly arrive, not just visit." },
            { label: "🌍 Extended adventure (2+ weeks)", value: "extended", response: "A true journey. You seek transformation, not just travel." }
        ],
        stateKey: 'duration',
        nextStep: 'priority'
    },
    {
        id: 'priority',
        text: "If you could carry only one memory home, what would it be?",
        expression: 'neutral',
        choices: [
            { label: "🍽️ An unforgettable meal", value: "food", response: "Taste is memory made physical." },
            { label: "🏞️ A breathtaking landscape", value: "nature", response: "Nature speaks to those who listen." },
            { label: "🤝 Connection with locals", value: "local", response: "The greatest journeys are measured in friendships." },
            { label: "📸 A perfect photograph", value: "photos", response: "To capture a moment is to honor it." }
        ],
        stateKey: 'priority',
        nextStep: 'result'
    }
];

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
    await typeText("The winds have chosen for you! Let me see what fate has in store...", dialogueText);
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

        // Energy match
        if (dest.energy === energy) score += 2;
        else if (dest.energy === 'medium' || energy === 'medium') score += 1;

        // Budget match
        if (dest.budget === budget) score += 2;
        else if ((dest.budget === 'mid' && budget !== 'high') || budget === 'mid') score += 1;

        // Duration match
        if (dest.idealDuration && dest.idealDuration.includes(duration)) score += 2;

        // Priority bonuses
        if (priority === 'food' && dest.vibes.includes('foodie')) score += 2;
        if (priority === 'nature' && dest.vibes.includes('nature')) score += 2;
        if (priority === 'local' && dest.vibes.includes('culture')) score += 1;
        if (priority === 'photos') score += 1;

        return { ...dest, score };
    });

    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, 3);
}

// Build destination card HTML
function buildDestinationCard(dest, index) {
    const isTopPick = index === 0;
    const durationLabel = {
        'weekend': '3-4 days',
        'week': '5-7 days',
        'extended': '2+ weeks'
    };

    return `
        <div class="destination-card ${isTopPick ? 'top-pick expanded' : ''}" data-id="${dest.id}">
            <div class="card-badge">Top Pick</div>
            <div class="card-header">
                <div class="card-image">${dest.icon}</div>
                <div class="card-info">
                    <div class="card-destination-name">${dest.name}</div>
                    <div class="card-tagline">"${dest.tagline}"</div>
                    <div class="card-tags">
                        ${dest.vibes.map(v => `<span class="card-tag">${v}</span>`).join('')}
                        <span class="card-tag">${dest.idealDuration.map(d => durationLabel[d]).join(' / ')}</span>
                    </div>
                </div>
            </div>
            <div class="card-details">
                <div class="trip-section">
                    <div class="trip-section-title">[ THINGS TO DO ]</div>
                    <div class="trip-section-content">
                        ${dest.activities.slice(0, 3).map(a => `<div class="trip-item">${a}</div>`).join('')}
                    </div>
                </div>
                <div class="trip-section">
                    <div class="trip-section-title">[ THINGS TO EAT ]</div>
                    <div class="trip-section-content">
                        ${dest.food.slice(0, 2).map(f => `<div class="trip-item">${f}</div>`).join('')}
                    </div>
                </div>
                <div class="trip-section">
                    <div class="trip-section-title">[ WHERE TO STAY ]</div>
                    <div class="trip-section-content">${dest.stay}</div>
                </div>
                <div class="tabiji-comment">
                    Tabiji's Wisdom: "${dest.tabijiComment}"
                </div>
            </div>
            <button class="expand-btn" onclick="toggleCard('${dest.id}')">
                ${isTopPick ? '▲ Show less' : '▼ Show details'}
            </button>
        </div>
    `;
}

// Toggle card expansion
function toggleCard(destId) {
    const card = document.querySelector(`.destination-card[data-id="${destId}"]`);
    const btn = card.querySelector('.expand-btn');
    const isExpanded = card.classList.contains('expanded');

    card.classList.toggle('expanded');
    btn.textContent = isExpanded ? '▼ Show details' : '▲ Show less';
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
    await typeText("The winds whisper to me...\n\n*ruffles feathers*\n\nYes. I see your path.", dialogueText);

    await sleep(400);

    const destinations = findBestDestinations();

    setExpression('excited');
    await typeText(`I have found ${destinations.length} paths for your journey:`, dialogueText);

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
