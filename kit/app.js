// === Tabiji Kit v0.1 — Emergency Travel Safety PWA ===

(function () {
  'use strict';

  // === State ===
  let countries = [];
  let currentCountry = null;
  let currentTab = 'emergency';
  let downloadedCountries = new Set();
  let deferredInstallPrompt = null;

  // === DOM refs ===
  const $ = (sel) => document.querySelector(sel);
  const listView = $('#listView');
  const detailView = $('#detailView');
  const searchInput = $('#searchInput');
  const countryList = $('#countryList');
  const backBtn = $('#backBtn');
  const offlineTag = $('#offlineTag');
  const installBanner = $('#installBanner');
  const installBtn = $('#installBtn');
  const installDismiss = $('#installDismiss');
  const countryHero = $('#countryHero');
  const tabsScroll = $('#tabsScroll');
  const tabContent = $('#tabContent');

  // === Tabs config ===
  const TABS = [
    { id: 'emergency', icon: '🚨', label: 'Emergency' },
    { id: 'embassies', icon: '🏛️', label: 'Embassies' },
    { id: 'advisories', icon: '⚠️', label: 'Advisories' },
    { id: 'healthcare', icon: '🏥', label: 'Healthcare' },
    { id: 'medications', icon: '💊', label: 'Medications' },
    { id: 'scams', icon: '🎭', label: 'Scams' },
    { id: 'phrases', icon: '🗣️', label: 'Phrases' },
    { id: 'practical', icon: '🔌', label: 'Practical' },
    { id: 'safety', icon: '🛡️', label: 'Safety' },
    { id: 'cards', icon: '💳', label: 'Card Coverage' },
    { id: 'maps', icon: '🗺️', label: 'Offline Maps' },
  ];

  // === Init ===
  async function init() {
    registerSW();
    await loadCountries();
    loadDownloadedState();
    renderCountryList();
    bindEvents();
    handleRoute();
    updateOnlineStatus();
  }

  // === Service Worker ===
  function registerSW() {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/kit/sw.js', { scope: '/kit/' })
        .then((reg) => console.log('SW registered:', reg.scope))
        .catch((err) => console.warn('SW registration failed:', err));

      navigator.serviceWorker.addEventListener('message', (e) => {
        if (e.data.type === 'COUNTRY_CACHED') {
          downloadedCountries.add(e.data.iso2);
          saveDownloadedState();
          renderCountryList();
          if (currentCountry && currentCountry.iso2 === e.data.iso2) {
            renderHero(currentCountry);
          }
        }
        if (e.data.type === 'COUNTRY_UNCACHED') {
          downloadedCountries.delete(e.data.iso2);
          saveDownloadedState();
          renderCountryList();
          if (currentCountry && currentCountry.iso2 === e.data.iso2) {
            renderHero(currentCountry);
          }
        }
        if (e.data.type === 'CACHE_ERROR') {
          alert('Failed to download country data. Check your connection.');
        }
      });
    }
  }

  // === Data Loading ===
  async function loadCountries() {
    try {
      const res = await fetch('/kit/data/countries.json');
      countries = await res.json();
    } catch (e) {
      console.error('Failed to load countries:', e);
      countries = [];
    }
  }

  async function loadCountryData(iso2) {
    const url = `/kit/data/safety/${iso2.toLowerCase()}.json`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Failed to load ${iso2}`);
    return res.json();
  }

  // === Downloaded State (localStorage) ===
  function loadDownloadedState() {
    try {
      const saved = localStorage.getItem('tabiji-kit-downloaded');
      if (saved) downloadedCountries = new Set(JSON.parse(saved));
    } catch (e) { /* ignore */ }
  }

  function saveDownloadedState() {
    localStorage.setItem('tabiji-kit-downloaded', JSON.stringify([...downloadedCountries]));
  }

  // === Rendering: Country List ===
  function renderCountryList(filter = '') {
    const q = filter.toLowerCase().trim();
    const filtered = q
      ? countries.filter((c) => c.name.toLowerCase().includes(q) || c.iso2.toLowerCase().includes(q))
      : countries;

    if (filtered.length === 0) {
      countryList.innerHTML = `
        <div class="no-results">
          <div class="no-results-emoji">🔍</div>
          <p>No countries found for "${escHtml(filter)}"</p>
        </div>`;
      return;
    }

    countryList.innerHTML = filtered.map((c) => `
      <li class="country-item" data-iso2="${c.iso2}">
        <span class="country-flag">${c.flag}</span>
        <div class="country-info">
          <div class="country-name">${escHtml(c.name)}</div>
          <div class="country-meta">${c.iso2}</div>
        </div>
        <span class="country-status">${downloadedCountries.has(c.iso2) ? '✅' : '›'}</span>
      </li>
    `).join('');
  }

  // === Rendering: Country Detail ===
  function renderHero(data) {
    const flag = countries.find((c) => c.iso2 === data.iso2)?.flag || '';
    const isDownloaded = downloadedCountries.has(data.iso2);
    countryHero.innerHTML = `
      <div class="country-hero-flag">${flag}</div>
      <h1 class="country-hero-name">${escHtml(data.name)}</h1>
      <div class="country-hero-actions">
        <button class="btn btn-primary ${isDownloaded ? 'downloaded' : ''}" id="downloadBtn" data-iso2="${data.iso2}">
          ${isDownloaded ? '✅ Downloaded' : '⬇️ Download Offline'}
        </button>
      </div>
    `;
  }

  function renderTabs() {
    tabsScroll.innerHTML = TABS.map((t) => `
      <button class="tab-btn ${t.id === currentTab ? 'active' : ''}" data-tab="${t.id}">
        ${t.icon} ${t.label}
      </button>
    `).join('');
  }

  function renderTabContent(data) {
    const html = TABS.map((t) => `
      <div class="tab-content ${t.id === currentTab ? 'active' : ''}" data-tab-content="${t.id}">
        ${renderTabSection(t.id, data)}
      </div>
    `).join('');
    tabContent.innerHTML = html;
  }

  function renderTabSection(tabId, d) {
    switch (tabId) {
      case 'emergency': return renderEmergency(d);
      case 'embassies': return renderEmbassies(d);
      case 'advisories': return renderAdvisories(d);
      case 'healthcare': return renderHealthcare(d);
      case 'medications': return renderMedications(d);
      case 'scams': return renderScams(d);
      case 'phrases': return renderPhrases(d);
      case 'practical': return renderPractical(d);
      case 'safety': return renderSafety(d);
      case 'cards': return renderCardCoverage(d);
      case 'maps': return renderOfflineMaps(d);
      default: return '<p>Coming soon</p>';
    }
  }

  // === Tab Renderers ===

  function renderEmergency(d) {
    const em = d.emergency || {};
    const cards = [];

    if (em.police) {
      cards.push(`
        <a href="tel:${em.police}" class="emergency-card police">
          <div class="emergency-icon">👮</div>
          <div class="emergency-label">Police</div>
          <div class="emergency-number">${escHtml(em.police)}</div>
        </a>`);
    }
    if (em.ambulance) {
      cards.push(`
        <a href="tel:${em.ambulance}" class="emergency-card ambulance">
          <div class="emergency-icon">🚑</div>
          <div class="emergency-label">Ambulance</div>
          <div class="emergency-number">${escHtml(em.ambulance)}</div>
        </a>`);
    }
    if (em.fire) {
      cards.push(`
        <a href="tel:${em.fire}" class="emergency-card fire">
          <div class="emergency-icon">🚒</div>
          <div class="emergency-label">Fire</div>
          <div class="emergency-number">${escHtml(em.fire)}</div>
        </a>`);
    }
    if (em.universal) {
      cards.push(`
        <a href="tel:${em.universal}" class="emergency-card universal">
          <div class="emergency-icon">📞</div>
          <div class="emergency-label">Universal Emergency</div>
          <div class="emergency-number">${escHtml(em.universal)}</div>
        </a>`);
    }

    let html = `<div class="emergency-grid">${cards.join('')}</div>`;
    if (em.notes) {
      html += `<div class="emergency-note">ℹ️ ${escHtml(em.notes)}</div>`;
    }
    return html;
  }

  function renderEmbassies(d) {
    const list = d.embassies || [];
    if (!list.length) return '<p>No embassy data available.</p>';

    return list.map((e) => `
      <div class="embassy-item">
        <div class="embassy-name">${escHtml(e.name)}</div>
        <span class="embassy-type">${escHtml(e.type || 'embassy')}</span>
        <div class="embassy-detail">
          <span class="embassy-detail-icon">📍</span>
          <span>${escHtml(e.address)}</span>
        </div>
        ${e.city ? `<div class="embassy-detail"><span class="embassy-detail-icon">🏙️</span><span>${escHtml(e.city)}</span></div>` : ''}
        ${e.email ? `<div class="embassy-detail"><span class="embassy-detail-icon">✉️</span><a href="mailto:${escHtml(e.email)}">${escHtml(e.email)}</a></div>` : ''}
        ${e.website ? `<div class="embassy-detail"><span class="embassy-detail-icon">🌐</span><a href="${escHtml(e.website)}" target="_blank" rel="noopener">Website</a></div>` : ''}
        <a href="tel:${escHtml(e.phone)}" class="embassy-phone">📞 ${escHtml(e.phone)}</a>
        ${e.emergencyPhone && e.emergencyPhone !== e.phone ? `<a href="tel:${escHtml(e.emergencyPhone)}" class="embassy-phone">🆘 Emergency: ${escHtml(e.emergencyPhone)}</a>` : ''}
      </div>
    `).join('');
  }

  function renderAdvisories(d) {
    let html = '';

    if (d.travelAdvisory) {
      const ta = d.travelAdvisory;
      const level = ta.level || 0;
      html += `
        <div class="advisory-card">
          <div class="advisory-source">🇺🇸 ${escHtml(ta.source)}</div>
          <div class="advisory-level advisory-level-${level}">
            Level ${level}: ${escHtml(ta.levelText || '')}
          </div>
          <p class="advisory-summary">${escHtml(ta.summary || '')}</p>
          ${ta.lastUpdated ? `<p style="font-size:0.75rem;color:var(--gray-500)">Updated: ${escHtml(ta.lastUpdated)}</p>` : ''}
          ${ta.url ? `<a href="${escHtml(ta.url)}" target="_blank" rel="noopener" class="advisory-link">View full advisory →</a>` : ''}
        </div>`;
    }

    if (d.travelAdvisoryUK) {
      const uk = d.travelAdvisoryUK;
      html += `
        <div class="advisory-card">
          <div class="advisory-source">🇬🇧 ${escHtml(uk.source)}</div>
          <p class="advisory-summary">${escHtml(uk.summary || '')}</p>
          ${uk.lastUpdated ? `<p style="font-size:0.75rem;color:var(--gray-500)">Updated: ${escHtml(uk.lastUpdated)}</p>` : ''}
          ${uk.url ? `<a href="${escHtml(uk.url)}" target="_blank" rel="noopener" class="advisory-link">View full advisory →</a>` : ''}
        </div>`;
    }

    return html || '<p>No advisory data available.</p>';
  }

  function renderHealthcare(d) {
    const h = d.healthcare || {};
    let html = '<div class="section-card">';

    if (h.systemType) {
      html += `<p><strong>System:</strong> ${escHtml(h.systemType)}</p>`;
    }
    if (h.qualityRating) {
      html += `<p><strong>Quality:</strong> <span class="health-rating ${h.qualityRating}">${escHtml(h.qualityRating)}</span></p>`;
    }
    if (h.walkInAccess !== undefined) {
      html += `<p><strong>Walk-in access:</strong> ${h.walkInAccess ? '✅ Yes' : '❌ No'}</p>`;
    }
    if (h.costForTourists) {
      html += `<p><strong>Cost for tourists:</strong> ${escHtml(h.costForTourists)}</p>`;
    }
    if (h.pharmacyAccess) {
      html += `<p><strong>Pharmacies:</strong> ${escHtml(h.pharmacyAccess)}</p>`;
    }
    if (h.hospitalNotes) {
      html += `<p><strong>Hospital notes:</strong> ${escHtml(h.hospitalNotes)}</p>`;
    }
    if (h.malariaRisk !== undefined) {
      html += `<p><strong>Malaria risk:</strong> ${h.malariaRisk ? '⚠️ Yes' : '✅ No'}</p>`;
    }
    if (h.insuranceAdvice) {
      html += `<div class="emergency-note" style="margin-top:12px">💡 ${escHtml(h.insuranceAdvice)}</div>`;
    }

    html += '</div>';

    if (h.vaccinationsRecommended && h.vaccinationsRecommended.length) {
      html += `
        <div class="section-card">
          <h3>💉 Recommended Vaccinations</h3>
          <div class="vaccine-list">
            ${h.vaccinationsRecommended.map((v) => `<span class="vaccine-tag">${escHtml(v)}</span>`).join('')}
          </div>
        </div>`;
    }

    if (d.hospitals && d.hospitals.length) {
      html += `<div class="section-card"><h3>🏥 Hospitals</h3>`;
      d.hospitals.forEach((hosp) => {
        html += `
          <div class="hospital-item">
            <div class="hospital-name">${escHtml(hosp.name)}</div>
            <div class="hospital-meta">
              ${escHtml(hosp.city)}${hosp.address ? ` · ${escHtml(hosp.address)}` : ''}
            </div>
            ${hosp.phone ? `<a href="tel:${escHtml(hosp.phone)}" class="hospital-phone">📞 ${escHtml(hosp.phone)}</a>` : ''}
            <div class="hospital-flags">
              ${hosp.open24h ? '<span class="hospital-flag">24h</span>' : ''}
              ${hosp.englishSpeaking ? '<span class="hospital-flag english">🇬🇧 English</span>' : ''}
              ${hosp.type === 'international' ? '<span class="hospital-flag intl">🌐 International</span>' : ''}
            </div>
            ${hosp.notes ? `<div class="hospital-notes">${escHtml(hosp.notes)}</div>` : ''}
          </div>`;
      });
      html += `</div>`;
    }

    return html;
  }

  function renderMedications(d) {
    const m = d.medications || {};
    let html = '';

    if (m.generalAdvice) {
      html += `<div class="emergency-note" style="margin-bottom:16px">⚠️ ${escHtml(m.generalAdvice)}</div>`;
    }

    if (m.yakkanShoumei || m['yakkan-shoumei']) {
      const ys = m.yakkanShoumei || m['yakkan-shoumei'];
      html += `<div class="section-card"><h3>📋 Import Certificate</h3><p>${escHtml(ys)}</p></div>`;
    }

    if (m.controlledSubstances && m.controlledSubstances.length) {
      html += m.controlledSubstances.map((s) => `
        <div class="med-item">
          <div class="med-name">
            ${escHtml(s.drug)}
            <span class="med-status ${s.status}">${escHtml(s.status)}</span>
          </div>
          <div class="med-note">${escHtml(s.note)}</div>
        </div>
      `).join('');
    }

    return html || '<p>No medication restriction data available.</p>';
  }

  function renderScams(d) {
    const scams = d.scams || [];
    if (!scams.length) return '<p>No scam data available for this country.</p>';

    return scams.map((s) => `
      <div class="scam-card">
        <div class="scam-name">${escHtml(s.name)}</div>
        <div class="scam-city">📍 ${escHtml(s.city || 'Nationwide')}</div>
        <div class="scam-desc">${escHtml(s.description)}</div>
        <div class="scam-avoid"><strong>✅ How to avoid:</strong> ${escHtml(s.avoidance)}</div>
      </div>
    `).join('');
  }

  function renderPhrases(d) {
    const phrases = d.phrases || [];
    if (!phrases.length) return '<p>No phrase data available.</p>';

    return phrases.map((p) => `
      <div class="phrase-item">
        <div class="phrase-english">${escHtml(p.english)}</div>
        <div class="phrase-local">${escHtml(p.local)}</div>
        <div class="phrase-phonetic">${escHtml(p.phonetic)}</div>
      </div>
    `).join('');
  }

  function renderPractical(d) {
    const p = d.practical || {};
    const c = d.cultural || {};
    const conn = d.connectivity || {};

    let html = '<div class="practical-grid">';

    const items = [
      { label: 'Tap Water', value: p.tapWater === true ? '✅ Safe' : p.tapWater === false ? '⚠️ Not Safe' : '—', full: false },
      { label: 'Driving Side', value: p.drivingSide ? capitalize(p.drivingSide) : '—', full: false },
      { label: 'Plug Type', value: p.plugType ? p.plugType.join(', ') : '—', full: false },
      { label: 'Voltage', value: p.voltage || '—', full: false },
      { label: 'Dial Code', value: p.dialCode || '—', full: false },
      { label: 'Time Zone', value: p.timeZone || '—', full: false },
    ];

    items.forEach((it) => {
      html += `
        <div class="practical-item ${it.full ? 'full-width' : ''}">
          <div class="practical-label">${it.label}</div>
          <div class="practical-value">${escHtml(it.value)}</div>
        </div>`;
    });

    html += '</div>';

    // Full-width items
    if (p.visaFreeCountries) {
      html += `<div class="section-card" style="margin-top:12px"><h3>🛂 Visa Info</h3><p>${escHtml(p.visaFreeCountries)}</p></div>`;
    }
    if (p.bestTimeToVisit) {
      html += `<div class="section-card"><h3>📅 Best Time to Visit</h3><p>${escHtml(p.bestTimeToVisit)}</p></div>`;
    }

    // Tipping
    if (c.tipping) {
      html += `<div class="section-card"><h3>💰 Tipping</h3><p>${escHtml(c.tipping)}</p></div>`;
    }

    // Connectivity
    if (conn.bestOption || conn.simOptions) {
      html += '<div class="section-card"><h3>📶 Connectivity</h3>';
      if (conn.bestOption) html += `<div class="connectivity-card"><h4>🏆 Best Option</h4><p>${escHtml(conn.bestOption)}</p></div>`;
      if (conn.simOptions) html += `<div class="connectivity-card"><h4>📱 SIM Options</h4><p>${escHtml(conn.simOptions)}</p></div>`;
      if (conn.wifiAvailability) html += `<div class="connectivity-card"><h4>📡 WiFi</h4><p>${escHtml(conn.wifiAvailability)}</p></div>`;
      html += '</div>';
    }

    // Cultural
    if (c.dressCode) {
      html += `<div class="section-card"><h3>👔 Dress Code</h3><p>${escHtml(c.dressCode)}</p></div>`;
    }
    if (c.greetings) {
      html += `<div class="section-card"><h3>👋 Greetings</h3><p>${escHtml(c.greetings)}</p></div>`;
    }
    if (c.haggling) {
      html += `<div class="section-card"><h3>🏷️ Haggling</h3><p>${escHtml(c.haggling)}</p></div>`;
    }
    if (c.taboos && c.taboos.length) {
      html += `<div class="section-card"><h3>🚫 Cultural Taboos</h3><ul class="taboo-list">${c.taboos.map((t) => `<li>${escHtml(t)}</li>`).join('')}</ul></div>`;
    }

    return html;
  }

  function renderSafety(d) {
    const s = d.safety || {};
    let html = '';

    if (s.overallRisk) {
      html += `
        <div class="section-card" style="text-align:center">
          <h3>Overall Risk</h3>
          <span class="risk-badge risk-${s.overallRisk}">${formatRisk(s.overallRisk)}</span>
        </div>`;
    }

    html += '<div class="safety-grid">';
    if (s.violentCrime) {
      html += `<div class="safety-metric"><div class="safety-metric-label">Violent Crime</div><span class="risk-badge risk-${s.violentCrime}">${formatRisk(s.violentCrime)}</span></div>`;
    }
    if (s.pettyCrime) {
      html += `<div class="safety-metric"><div class="safety-metric-label">Petty Crime</div><span class="risk-badge risk-${s.pettyCrime}">${formatRisk(s.pettyCrime)}</span></div>`;
    }
    html += '</div>';

    if (s.naturalDisasters && s.naturalDisasters.length) {
      html += `
        <div class="section-card">
          <h3>🌋 Natural Disaster Risks</h3>
          <div class="disaster-list">
            ${s.naturalDisasters.map((nd) => `<span class="disaster-tag">${escHtml(nd)}</span>`).join('')}
          </div>
        </div>`;
    }

    if (d.disasterResponse && d.disasterResponse.protocols && d.disasterResponse.protocols.length) {
      html += `<div class="section-card"><h3>🆘 Emergency Protocols</h3>`;
      d.disasterResponse.protocols.forEach((p) => {
        html += `
          <div class="protocol-item">
            <div class="protocol-type">${escHtml(p.type)}</div>
            ${p.immediate && p.immediate.length ? `
              <div class="protocol-section"><strong>Immediate actions:</strong>
                <ul>${p.immediate.map((a) => `<li>${escHtml(a)}</li>`).join('')}</ul>
              </div>` : ''}
            ${p.resources && p.resources.length ? `
              <div class="protocol-resources">${p.resources.map((r) => `<small>${escHtml(r)}</small>`).join('<br>')}</div>` : ''}
          </div>`;
      });
      html += `</div>`;
    }

    if (s.lgbtSafety) {
      html += `<div class="section-card"><h3>🏳️‍🌈 LGBTQ+ Safety</h3><p>${escHtml(s.lgbtSafety)}</p></div>`;
    }

    if (s.soloFemaleSafety) {
      html += `<div class="section-card"><h3>👩 Solo Female Safety</h3><p>${escHtml(s.soloFemaleSafety)}</p></div>`;
    }

    if (s.notes) {
      html += `<div class="emergency-note" style="margin-top:12px">📝 ${escHtml(s.notes)}</div>`;
    }

    return html || '<p>No safety data available.</p>';
  }

  function renderCardCoverage(d) {
    const cc = d.cardCoverage || {};
    const topCards = cc.topCards || [];
    if (!topCards.length) return '<p>No card coverage data available for this country.</p>';

    let html = `<div class="section-card"><h3>Best cards for ${escHtml(d.name)}</h3>`;
    topCards.forEach((card) => {
      html += `
        <div class="card-coverage-item">
          <div class="card-coverage-name">${escHtml(card.name)}</div>
          <div class="card-coverage-benefits">${escHtml((card.relevantBenefits || []).join(', '))}</div>
        </div>`;
    });
    html += '</div>';
    return html;
  }

  function renderOfflineMaps(d) {
    const mi = d.mapIntegration || {};
    let html = '<div class="section-card"><h3>Offline Map Setup</h3>';

    if (mi.offlineTileSizeEstimate) {
      html += `<p><strong>Estimated download size:</strong> ${escHtml(mi.offlineTileSizeEstimate)}</p>`;
    }
    if (mi.recommendedZoom) {
      const z = mi.recommendedZoom;
      html += `<p><strong>Recommended zoom levels:</strong> City: z${escHtml(String(z.city || ''))}, Country: z${escHtml(String(z.country || ''))}</p>`;
    }

    html += `
      <p><strong>Embassy coordinates:</strong> ${mi.embassyCoordinatesAvailable ? '✅ Available in this profile' : '—'}</p>
      <p><strong>Coordinate system:</strong> WGS84 (decimal degrees)</p>
    </div>`;

    html += `
      <div class="section-card">
        <h3>Recommended: OpenStreetMap + Leaflet.js</h3>
        <p>Free, open-license map tiles. Cache via service worker for offline use.</p>
        <p style="font-size:0.8rem;color:var(--gray-500)">Tile URL: https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png</p>
        <p style="font-size:0.8rem;color:var(--gray-500)">Offline plugin: leaflet.offline (allartk/leaflet.offline)</p>
        <p style="font-size:0.8rem;color:var(--gray-500)">~200 tiles at z13 per city ≈ 2MB</p>
      </div>
      <div class="section-card">
        <h3>Full Provider Guide</h3>
        <p style="font-size:0.875rem">See <code>/api/v1/offline-maps.json</code> for detailed integration guidance for OSM, Mapbox, Google Maps, and Apple Maps.</p>
      </div>`;

    return html;
  }

  // === Helpers ===
  function escHtml(str) {
    if (!str) return '';
    const d = document.createElement('div');
    d.textContent = String(str);
    return d.innerHTML;
  }

  function formatRisk(risk) {
    if (!risk) return '—';
    return risk.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  }

  function capitalize(s) {
    return s ? s.charAt(0).toUpperCase() + s.slice(1) : '';
  }

  // === Navigation ===
  function showList() {
    currentCountry = null;
    listView.classList.add('active');
    detailView.classList.remove('active');
    backBtn.classList.remove('visible');
    window.history.pushState({}, '', '/kit/');
    document.title = 'Tabiji Kit 🧳';
    searchInput.focus();
  }

  async function showCountry(iso2) {
    listView.classList.remove('active');
    detailView.classList.add('active');
    backBtn.classList.add('visible');

    // Show loading
    countryHero.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading...</p></div>';
    tabsScroll.innerHTML = '';
    tabContent.innerHTML = '';

    try {
      const data = await loadCountryData(iso2);
      currentCountry = data;
      currentTab = 'emergency';

      renderHero(data);
      renderTabs();
      renderTabContent(data);

      window.history.pushState({ iso2 }, '', `/kit/${iso2.toLowerCase()}`);
      document.title = `${data.name} — Tabiji Kit`;
      window.scrollTo(0, 0);
    } catch (e) {
      countryHero.innerHTML = `
        <div class="loading">
          <p>❌ Failed to load country data</p>
          <p style="font-size:0.875rem;margin-top:8px">${navigator.onLine ? 'Try again later.' : 'You\'re offline. Download this country first.'}</p>
        </div>`;
    }
  }

  function switchTab(tabId) {
    currentTab = tabId;
    tabsScroll.querySelectorAll('.tab-btn').forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.tab === tabId);
    });
    tabContent.querySelectorAll('.tab-content').forEach((tc) => {
      tc.classList.toggle('active', tc.dataset.tabContent === tabId);
    });

    // Scroll the active tab into view
    const activeTab = tabsScroll.querySelector('.tab-btn.active');
    if (activeTab) {
      activeTab.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
    }
  }

  // === Routing ===
  function handleRoute() {
    const path = window.location.pathname.replace(/^\/kit\/?/, '').replace(/\/$/, '');
    if (path && path.length === 2) {
      showCountry(path.toUpperCase());
    }
  }

  // === Events ===
  function bindEvents() {
    // Search
    searchInput.addEventListener('input', () => {
      renderCountryList(searchInput.value);
    });

    // Country list click
    countryList.addEventListener('click', (e) => {
      const item = e.target.closest('.country-item');
      if (item) showCountry(item.dataset.iso2);
    });

    // Back button
    backBtn.addEventListener('click', showList);

    // Tab clicks
    tabsScroll.addEventListener('click', (e) => {
      const btn = e.target.closest('.tab-btn');
      if (btn) switchTab(btn.dataset.tab);
    });

    // Download button (delegated)
    document.addEventListener('click', (e) => {
      const dlBtn = e.target.closest('#downloadBtn');
      if (dlBtn) {
        const iso2 = dlBtn.dataset.iso2;
        if (downloadedCountries.has(iso2)) {
          // Remove from cache
          if (navigator.serviceWorker.controller) {
            navigator.serviceWorker.controller.postMessage({
              type: 'UNCACHE_COUNTRY',
              iso2,
              url: `/kit/data/safety/${iso2.toLowerCase()}.json`,
            });
          }
        } else {
          // Download
          dlBtn.textContent = '⏳ Downloading...';
          dlBtn.disabled = true;
          if (navigator.serviceWorker.controller) {
            navigator.serviceWorker.controller.postMessage({
              type: 'CACHE_COUNTRY',
              iso2,
              url: `/kit/data/safety/${iso2.toLowerCase()}.json`,
            });
          } else {
            // Fallback: just mark as downloaded in localStorage
            downloadedCountries.add(iso2);
            saveDownloadedState();
            renderHero(currentCountry);
            renderCountryList();
          }
        }
      }
    });

    // Browser back/forward
    window.addEventListener('popstate', () => {
      const path = window.location.pathname.replace(/^\/kit\/?/, '').replace(/\/$/, '');
      if (path && path.length === 2) {
        showCountry(path.toUpperCase());
      } else {
        showList();
      }
    });

    // Online/offline
    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);

    // PWA install
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      deferredInstallPrompt = e;
      if (!localStorage.getItem('tabiji-kit-install-dismissed')) {
        installBanner.classList.add('visible');
      }
    });

    installBtn.addEventListener('click', () => {
      if (deferredInstallPrompt) {
        deferredInstallPrompt.prompt();
        deferredInstallPrompt.userChoice.then(() => {
          deferredInstallPrompt = null;
          installBanner.classList.remove('visible');
        });
      }
    });

    installDismiss.addEventListener('click', () => {
      installBanner.classList.remove('visible');
      localStorage.setItem('tabiji-kit-install-dismissed', '1');
    });
  }

  function updateOnlineStatus() {
    offlineTag.classList.toggle('visible', !navigator.onLine);
  }

  // === Boot ===
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
