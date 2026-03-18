const deckSlides = [
  ['Tabiji Quest', 'Plan a trip by playing one. A travel-planning game where players roleplay a traveler, talk to an expert guide, make decisions, and end with an itinerary they’d actually want to take.'],
  ['The problem', 'Travel planning starts dead: blank search boxes, walls of filters, or generic chat. Inspiration is weak and planning feels like work too early.'],
  ['The insight', 'People discover what they want by reacting. It is easier to choose between routes and tradeoffs than describe a perfect trip from scratch.'],
  ['The product', 'A travel product wrapped in a game: scenario setup, opinionated guide, route choices, activity tradeoffs, and a coherent trip payoff.'],
  ['Why it fits Tabiji', 'It turns recommendation, itinerary logic, and travel taste into a differentiated top-of-funnel experience with structured preference capture.'],
  ['What the user sees', 'Pick scenario, set mood and budget, talk to guide, make route decisions, watch stats move, end with route + itinerary handoff.'],
  ['Why better than normal chat', 'Chat is just the interface. Structured state is the product. That means coherent recommendations, visible tradeoffs, and better conversion intent.'],
  ['The MVP', 'One scenario. One guide. Chat + choice cards. Light stats. End-of-run itinerary export. Enough to prove the magic without building nonsense.'],
  ['Why Japan first', 'Massive demand, strong route tradeoffs, obvious food/culture/city/calm contrasts, and perfect conditions for a guide with actual opinions.'],
  ['User value', 'The player leaves with a clearer sense of travel taste, a route that fits, and confidence about tradeoffs — not just a cute transcript.'],
  ['Business value', 'More top-of-funnel engagement, richer preference data, stronger differentiation, and a more playful entry into real planning.'],
  ['Metrics', 'Measure play-start rate, completion, average turns, replay rate, share rate, and itinerary CTA clickthrough.'],
  ['Risks', 'Too much AI improv creates mush. Too much simulation creates homework. Too little utility creates a toy.'],
  ['Mitigation', 'Use scripted branching first, keep the guide voice sharp, constrain destination logic, and make itinerary handoff core to the MVP.'],
  ['Recommendation', 'Build one polished, opinionated web scenario first. Do not build an open-world travel game. Do not build a generic AI concierge.']
];

const STORAGE_KEY = 'tabiji-quest-session-v1';
const HANDOFF_KEY = 'tabiji-quest-handoff-v1';

const ui = {
  chatLog: document.getElementById('chatLog'),
  cards: document.getElementById('cards'),
  choices: document.getElementById('choices'),
  eventBadge: document.getElementById('eventBadge'),
  gameScreen: document.getElementById('game-screen'),
  summaryScreen: document.getElementById('summary-screen'),
  statusNote: document.getElementById('statusNote'),
  budgetLabel: document.getElementById('budgetLabel'),
  daysLabel: document.getElementById('daysLabel'),
  energyLabel: document.getElementById('energyLabel'),
  fitLabel: document.getElementById('fitLabel'),
  budgetBar: document.getElementById('budgetBar'),
  daysBar: document.getElementById('daysBar'),
  energyBar: document.getElementById('energyBar'),
  fitBar: document.getElementById('fitBar'),
  routeBox: document.getElementById('routeBox'),
  travelerType: document.getElementById('travelerType'),
  finalRoute: document.getElementById('finalRoute'),
  bestSplurge: document.getElementById('bestSplurge'),
  biggestWin: document.getElementById('biggestWin'),
  summaryText: document.getElementById('summaryText'),
  scoreBudget: document.getElementById('scoreBudget'),
  scoreEnergy: document.getElementById('scoreEnergy'),
  scoreTaste: document.getElementById('scoreTaste'),
  scoreChaos: document.getElementById('scoreChaos'),
  inferredPrefs: document.getElementById('inferredPrefs'),
  payloadBox: document.getElementById('payloadBox'),
  deckSlides: document.getElementById('slides'),
  slideCount: document.getElementById('slideCount'),
  handoffButton: document.getElementById('handoff'),
  copyPayloadButton: document.getElementById('copyPayload'),
  downloadPayloadButton: document.getElementById('downloadPayload'),
  openPlannerButton: document.getElementById('openPlanner'),
  clearSavedButton: document.getElementById('clearSaved'),
  resumeButton: document.getElementById('resumeGame'),
  startButton: document.getElementById('start-game'),
  progressLabel: document.getElementById('progressLabel'),
  progressBar: document.getElementById('progressBar'),
  turnMeta: document.getElementById('turnMeta')
};

const state = {
  scenario: null,
  turnMap: new Map(),
  session: null,
  currentSlide: 0,
  selectedSetup: {
    style: 'Food and atmosphere',
    budgetBand: 'Comfortable',
    priority: 'Maximize memories'
  },
  handoffPayload: null
};

function track(eventName, payload = {}) {
  const enriched = {
    surface: 'tmp-travel-game',
    scenarioId: state.session?.scenarioId || state.scenario?.scenario?.id || null,
    ...payload
  };

  if (typeof window.gtag === 'function') {
    window.gtag('event', eventName, enriched);
  }

  if (Array.isArray(window.dataLayer)) {
    window.dataLayer.push({ event: eventName, ...enriched });
  }

  console.info('[travel-game-event]', eventName, enriched);
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function uniq(items = []) {
  return [...new Set(items)];
}

function setStatus(message, isError = false) {
  ui.statusNote.textContent = message;
  ui.statusNote.classList.toggle('error', isError);
}

function saveSession() {
  if (!state.session) return;
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({
      session: state.session,
      selectedSetup: state.selectedSetup,
      handoffPayload: state.handoffPayload,
      savedAt: Date.now()
    })
  );
  ui.resumeButton.disabled = false;
}

function clearSavedSession() {
  localStorage.removeItem(STORAGE_KEY);
  ui.resumeButton.disabled = true;
  setStatus('Saved run cleared.');
}

function loadSavedSession() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

async function copyText(text) {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
    return true;
  }
  return false;
}

function downloadPayload() {
  if (!state.handoffPayload) return;
  const blob = new Blob([JSON.stringify(state.handoffPayload, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${state.handoffPayload.scenarioId}-handoff.json`;
  a.click();
  URL.revokeObjectURL(url);
}

function openPlanner() {
  if (!state.handoffPayload) return;
  localStorage.setItem(HANDOFF_KEY, JSON.stringify(state.handoffPayload));
  const encoded = encodeURIComponent(JSON.stringify({
    source: state.handoffPayload.source,
    scenarioId: state.handoffPayload.scenarioId,
    route: state.handoffPayload.route,
    travelerType: state.handoffPayload.travelerType
  }));
  window.open(`/plan.html?tabijiQuest=${encoded}`, '_blank', 'noopener');
}

async function loadScenario() {
  const response = await fetch('./content/japan-first-timer.json');
  if (!response.ok) throw new Error(`Failed to load scenario: ${response.status}`);
  const data = await response.json();
  state.scenario = data;
  state.turnMap = new Map(data.turns.map((turn) => [turn.id, turn]));
  renderScenarioMeta();
}

function renderScenarioMeta() {
  const scenario = state.scenario.scenario;
  document.getElementById('scenarioTitle').textContent = scenario.title;
  document.getElementById('scenarioSummary').textContent = scenario.summary;
  ui.handoffButton.textContent = 'Turn this into a real itinerary';
}

function hydrateSetupChips() {
  document.querySelectorAll('.chips').forEach((group) => {
    const key = group.dataset.group;
    const stateKey = key === 'budget' ? 'budgetBand' : key;
    group.querySelectorAll('.chip').forEach((chip) => {
      chip.classList.toggle('active', chip.dataset.value === state.selectedSetup[stateKey]);
    });
  });
}

function initSession() {
  const scenario = state.scenario.scenario;
  const startState = structuredClone(scenario.startState);
  state.session = {
    scenarioId: scenario.id,
    currentTurnId: scenario.turnOrder[0],
    stats: startState.stats,
    route: startState.route,
    flags: startState.flags,
    discoveredPreferences: startState.discoveredPreferences,
    decisions: {},
    eventHistory: [],
    completed: false,
    endingId: null,
    selectedSetup: { ...state.selectedSetup }
  };
  state.handoffPayload = null;
  ui.chatLog.innerHTML = '';
  ui.cards.innerHTML = '';
  ui.choices.innerHTML = '';
  ui.eventBadge.classList.add('hidden');
  ui.summaryScreen.classList.add('hidden');
  ui.gameScreen.classList.remove('hidden');
  ui.payloadBox.textContent = 'Handoff payload will appear here when the run completes.';
  ui.copyPayloadButton.disabled = true;
  ui.downloadPayloadButton.disabled = true;
  ui.openPlannerButton.disabled = true;
  setStatus('Scenario loaded from JSON. Session persistence, analytics hooks, and a real handoff path are now wired in.');
  updateStats();
  saveSession();
  track('travel_game_started', { setup: state.selectedSetup });
  renderCurrentTurn();
}

function restoreSession(saved) {
  state.selectedSetup = saved.selectedSetup || state.selectedSetup;
  state.session = saved.session;
  state.handoffPayload = saved.handoffPayload || null;
  hydrateSetupChips();
  ui.chatLog.innerHTML = '';
  ui.cards.innerHTML = '';
  ui.choices.innerHTML = '';
  ui.eventBadge.classList.add('hidden');
  ui.gameScreen.classList.remove('hidden');
  ui.summaryScreen.classList.add('hidden');
  updateStats();
  setStatus('Resumed saved session from localStorage.');
  track('travel_game_resumed', { currentTurnId: state.session.currentTurnId, completed: state.session.completed });
  if (state.session.completed) {
    const endingTurn = state.turnMap.get('ending');
    renderEnding(endingTurn);
  } else {
    renderCurrentTurn();
  }
}

function updateStats() {
  const { budget, daysRemaining, energy, styleFit } = state.session.stats;
  ui.budgetLabel.textContent = budget;
  ui.daysLabel.textContent = daysRemaining;
  ui.energyLabel.textContent = energy;
  ui.fitLabel.textContent = styleFit;
  ui.budgetBar.style.width = `${clamp(budget, 0, 100)}%`;
  ui.daysBar.style.width = `${clamp((daysRemaining / state.scenario.scenario.tripLengthDays) * 100, 0, 100)}%`;
  ui.energyBar.style.width = `${clamp(energy, 0, 100)}%`;
  ui.fitBar.style.width = `${clamp(styleFit, 0, 100)}%`;
  ui.routeBox.textContent = state.session.route.length ? state.session.route.join(' → ') : 'No route locked yet.';
}

function addMessage(text, role) {
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  div.textContent = text;
  ui.chatLog.appendChild(div);
  ui.chatLog.scrollTop = ui.chatLog.scrollHeight;
}

function renderDestinationCards(cardIds = []) {
  ui.cards.innerHTML = '';
  cardIds.forEach((id) => {
    const card = state.scenario.destinationCards[id];
    if (!card) return;
    const el = document.createElement('div');
    el.className = 'card';
    el.innerHTML = `
      <div class="card-title">${card.title}</div>
      <div class="muted">Best for: ${card.bestFor.join(', ')}</div>
      <div class="muted" style="margin-top:6px;">Tradeoff: ${card.tradeoff}</div>
      <div class="muted" style="margin-top:6px;">Great pairing: ${card.greatPairings.join(', ')}</div>
    `;
    ui.cards.appendChild(el);
  });
}

function countCompletedTurns() {
  return Object.keys(state.session.decisions).length;
}

function renderProgress(turn) {
  const totalTurns = state.scenario.scenario.turnOrder.length - 1;
  const completed = countCompletedTurns();
  const progressPct = clamp((completed / totalTurns) * 100, 0, 100);
  ui.progressLabel.textContent = `Turn ${completed + 1} of ${totalTurns}`;
  ui.progressBar.style.width = `${progressPct}%`;
  ui.turnMeta.textContent = `${turn.phase} · ${state.scenario.scenario.guide.name} is steering this run with deterministic state underneath the copy.`;
}

function renderCurrentTurn() {
  const turn = state.turnMap.get(state.session.currentTurnId);
  if (!turn) {
    setStatus(`Missing turn: ${state.session.currentTurnId}`, true);
    return;
  }

  if (turn.phase === 'ending') {
    renderEnding(turn);
    return;
  }

  ui.choices.innerHTML = '';
  ui.eventBadge.classList.add('hidden');
  if (turn.eventBanner) {
    ui.eventBadge.textContent = turn.eventBanner;
    ui.eventBadge.classList.remove('hidden');
  }

  renderProgress(turn);
  addMessage(turn.guideMessage, 'guide');
  renderDestinationCards(turn.destinationCards || []);

  turn.choices.forEach((choice) => {
    const delta = [];
    if (choice.effects?.budget) delta.push(`budget ${choice.effects.budget > 0 ? '+' : ''}${choice.effects.budget}`);
    if (choice.effects?.daysRemaining) delta.push(`days ${choice.effects.daysRemaining > 0 ? '+' : ''}${choice.effects.daysRemaining}`);
    if (choice.effects?.energy) delta.push(`energy ${choice.effects.energy > 0 ? '+' : ''}${choice.effects.energy}`);
    if (choice.effects?.styleFit) delta.push(`fit ${choice.effects.styleFit > 0 ? '+' : ''}${choice.effects.styleFit}`);
    const el = document.createElement('div');
    el.className = 'choice';
    el.innerHTML = `<div class="card-title">${choice.label}</div><div class="muted">${delta.length ? delta.join(' · ') : 'No stat change preview'}.</div>`;
    el.onclick = () => applyChoice(turn, choice);
    ui.choices.appendChild(el);
  });
}

function applyEffects(effects = {}) {
  const stats = state.session.stats;
  if (typeof effects.budget === 'number') stats.budget = clamp(stats.budget + effects.budget, 0, 100);
  if (typeof effects.daysRemaining === 'number') stats.daysRemaining = Math.max(0, stats.daysRemaining + effects.daysRemaining);
  if (typeof effects.energy === 'number') stats.energy = clamp(stats.energy + effects.energy, 0, 100);
  if (typeof effects.satisfaction === 'number') stats.satisfaction = clamp(stats.satisfaction + effects.satisfaction, 0, 100);
  if (typeof effects.styleFit === 'number') stats.styleFit = clamp(stats.styleFit + effects.styleFit, 0, 100);
}

function applyChoice(turn, choice) {
  addMessage(choice.playerReply, 'player');
  state.session.decisions[turn.id] = choice.id;
  applyEffects(choice.effects);

  if (choice.setRoute) state.session.route = [...choice.setRoute];
  if (choice.appendRoute) state.session.route = uniq([...state.session.route, ...choice.appendRoute]);
  if (choice.setFlags) state.session.flags = uniq([...state.session.flags, ...choice.setFlags]);
  if (choice.discover) state.session.discoveredPreferences = uniq([...state.session.discoveredPreferences, ...choice.discover]);
  if (choice.eventBanner) {
    state.session.eventHistory = uniq([...state.session.eventHistory, choice.eventBanner]);
    ui.eventBadge.textContent = choice.eventBanner;
    ui.eventBadge.classList.remove('hidden');
  }

  updateStats();
  saveSession();
  track('travel_game_choice_selected', {
    turnId: turn.id,
    choiceId: choice.id,
    routeLength: state.session.route.length,
    stats: state.session.stats
  });

  state.session.currentTurnId = choice.nextTurnId;
  window.setTimeout(renderCurrentTurn, 150);
}

function matchesEnding(ending) {
  const rules = ending.when || {};
  const flags = state.session.flags;
  const stats = state.session.stats;
  if (rules.allFlags && !rules.allFlags.every((flag) => flags.includes(flag))) return false;
  if (rules.anyFlags && !rules.anyFlags.some((flag) => flags.includes(flag))) return false;
  if (typeof rules.minStyleFit === 'number' && stats.styleFit < rules.minStyleFit) return false;
  if (typeof rules.maxStyleFit === 'number' && stats.styleFit > rules.maxStyleFit) return false;
  if (typeof rules.minEnergy === 'number' && stats.energy < rules.minEnergy) return false;
  if (typeof rules.maxEnergy === 'number' && stats.energy > rules.maxEnergy) return false;
  if (typeof rules.minBudget === 'number' && stats.budget < rules.minBudget) return false;
  if (typeof rules.maxBudget === 'number' && stats.budget > rules.maxBudget) return false;
  return true;
}

function resolveEnding(turn) {
  const variant = (turn.endingVariants || []).find(matchesEnding);
  if (variant) return variant;
  return { id: 'default-ending', ...turn.defaultEnding };
}

function buildHandoffPayload(ending) {
  const scenarioMeta = state.scenario.scenario;
  return {
    source: 'tabiji-quest',
    scenarioId: scenarioMeta.id,
    scenarioTitle: scenarioMeta.title,
    route: state.session.route,
    tripLengthDays: scenarioMeta.tripLengthDays,
    stats: state.session.stats,
    flags: state.session.flags,
    discoveredPreferences: state.session.discoveredPreferences,
    travelerType: ending.travelerType,
    summary: ending.summary,
    ctaLabel: ending.cta,
    guideId: scenarioMeta.guide.id,
    guideName: scenarioMeta.guide.name,
    contentVersion: scenarioMeta.version,
    selectedSetup: state.session.selectedSetup,
    decisions: state.session.decisions,
    eventHistory: state.session.eventHistory
  };
}

function computeBestSplurge() {
  if (state.session.flags.includes('splurge-ryokan')) return 'A ryokan night with actual emotional payoff';
  if (state.session.flags.includes('splurge-meal')) return 'One meal worth building a scene around';
  if (state.session.flags.includes('splurge-hotel')) return 'A smarter hotel location that saved the whole trip';
  return 'No deliberate splurge selected';
}

function renderEnding(turn) {
  const ending = resolveEnding(turn);
  state.session.completed = true;
  state.session.endingId = ending.id;
  state.handoffPayload = buildHandoffPayload(ending);
  saveSession();
  ui.gameScreen.classList.add('hidden');
  ui.summaryScreen.classList.remove('hidden');
  ui.travelerType.textContent = ending.travelerType;
  ui.finalRoute.textContent = state.session.route.length ? state.session.route.join(' → ') : 'Tokyo → Kyoto';
  ui.bestSplurge.textContent = computeBestSplurge();
  ui.biggestWin.textContent = ending.biggestWin;
  ui.summaryText.textContent = ending.summary;
  ui.scoreBudget.textContent = `${Math.max(1, Math.round(state.session.stats.budget / 10))}/10`;
  ui.scoreEnergy.textContent = `${Math.max(1, Math.round(state.session.stats.energy / 10))}/10`;
  ui.scoreTaste.textContent = `${Math.max(1, Math.round(state.session.stats.styleFit / 10))}/10`;
  ui.scoreChaos.textContent = `${state.session.route.length <= 2 ? '10/10' : '7/10'}`;
  ui.inferredPrefs.innerHTML = '';
  const prefs = state.session.discoveredPreferences.length ? state.session.discoveredPreferences : ['No strong preferences discovered yet'];
  prefs.forEach((pref) => {
    const item = document.createElement('div');
    item.className = 'list-item';
    item.textContent = pref;
    ui.inferredPrefs.appendChild(item);
  });
  ui.payloadBox.textContent = JSON.stringify(state.handoffPayload, null, 2);
  ui.handoffButton.textContent = ending.cta;
  ui.copyPayloadButton.disabled = false;
  ui.downloadPayloadButton.disabled = false;
  ui.openPlannerButton.disabled = false;
  track('travel_game_completed', {
    endingId: ending.id,
    route: state.session.route,
    stats: state.session.stats
  });
}

function renderSlides() {
  ui.deckSlides.innerHTML = '';
  const [title, body] = deckSlides[state.currentSlide];
  const slide = document.createElement('div');
  slide.className = 'slide';
  slide.innerHTML = `<div class="eyebrow">Slide ${state.currentSlide + 1}</div><div class="slide-title">${title}</div><div class="muted" style="line-height:1.6;">${body}</div>`;
  ui.deckSlides.appendChild(slide);
  ui.slideCount.textContent = `Slide ${state.currentSlide + 1} of ${deckSlides.length}`;
}

function wireSetupChips() {
  document.querySelectorAll('.chips').forEach((group) => {
    group.addEventListener('click', (e) => {
      const chip = e.target.closest('.chip');
      if (!chip) return;
      group.querySelectorAll('.chip').forEach((c) => c.classList.remove('active'));
      chip.classList.add('active');
      const key = group.dataset.group;
      state.selectedSetup[key === 'budget' ? 'budgetBand' : key] = chip.dataset.value;
    });
  });
}

function wireButtons() {
  ui.startButton.onclick = initSession;
  document.getElementById('replay').onclick = initSession;
  ui.resumeButton.onclick = () => {
    const saved = loadSavedSession();
    if (saved?.session) restoreSession(saved);
  };
  ui.clearSavedButton.onclick = clearSavedSession;
  ui.handoffButton.onclick = () => {
    track('travel_game_itinerary_cta_clicked', {
      endingId: state.session?.endingId
    });
    openPlanner();
  };
  ui.copyPayloadButton.onclick = async () => {
    if (!state.handoffPayload) return;
    const ok = await copyText(JSON.stringify(state.handoffPayload, null, 2));
    setStatus(ok ? 'Handoff payload copied to clipboard.' : 'Clipboard API unavailable here.', !ok);
    track('travel_game_payload_copied', { success: ok });
  };
  ui.downloadPayloadButton.onclick = () => {
    downloadPayload();
    setStatus('Downloaded handoff payload JSON.');
    track('travel_game_payload_downloaded');
  };
  ui.openPlannerButton.onclick = () => {
    openPlanner();
    setStatus('Opened plan.html with a lightweight travel-game handoff payload.');
    track('travel_game_planner_opened');
  };
  document.getElementById('prevSlide').onclick = () => {
    state.currentSlide = (state.currentSlide - 1 + deckSlides.length) % deckSlides.length;
    renderSlides();
  };
  document.getElementById('nextSlide').onclick = () => {
    state.currentSlide = (state.currentSlide + 1) % deckSlides.length;
    renderSlides();
  };
  document.getElementById('jump-play').onclick = () => document.getElementById('play-panel').scrollIntoView({ behavior: 'smooth' });
  document.getElementById('jump-deck').onclick = () => document.getElementById('deck-panel').scrollIntoView({ behavior: 'smooth' });
}

async function bootstrap() {
  wireSetupChips();
  wireButtons();
  renderSlides();
  try {
    await loadScenario();
    const saved = loadSavedSession();
    ui.resumeButton.disabled = !saved?.session;
    if (saved?.session) {
      state.selectedSetup = saved.selectedSetup || state.selectedSetup;
      hydrateSetupChips();
      setStatus('Saved session found. You can resume where you left off or start a fresh run.');
    }
    initSession();
    track('travel_game_viewed');
  } catch (error) {
    console.error(error);
    setStatus(error.message, true);
  }
}

bootstrap();
