/* Nav dropdown close on outside click */
document.addEventListener('click',function(e){document.querySelectorAll('.nav-dropdown.open').forEach(function(d){if(!d.contains(e.target))d.classList.remove('open')})});

/* TOC active state tracking */
const sections = document.querySelectorAll('[id]');
const tocLinks = document.querySelectorAll('.toc-sidebar a, .toc-mobile-dropdown a');
const mobileLabel = document.querySelector('.toc-active-label');
const ticker = document.getElementById('score-ticker');
const tickerSection = document.getElementById('ticker-section');
const jumpBtn = document.getElementById('jump-verdict');

/* Section name map for ticker */
const sectionNames = {
    'quick-answers':'Quick Answers','the-tl-dr-verdict':'Verdict','scorecard':'Scorecard',
    'city-character':'City Character','architecture-culture':'Architecture','food-dining':'Food',
    'beaches':'Beaches','cost-comparison':'Costs','getting-around':'Transport',
    'neighborhoods':'Neighborhoods','nightlife':'Nightlife','best-time':'Best Time',
    'day-trips':'Day Trips','safety':'Safety','the-decision-framework':'Decision',
    'frequently-asked-questions':'FAQ'
};

function updateTOC() {
    let current = '';
    sections.forEach(function(s) {
        if (s.getBoundingClientRect().top <= 120) current = s.id;
    });
    tocLinks.forEach(function(link) {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + current) {
            link.classList.add('active');
            if (mobileLabel && link.closest('.toc-mobile-dropdown')) {
                mobileLabel.textContent = link.textContent;
            }
        }
    });
    /* Sticky score ticker — show after scrolling past hero */
    var heroBottom = document.querySelector('.hero').getBoundingClientRect().bottom;
    if (heroBottom < 0) {
        ticker.classList.add('visible');
        if (sectionNames[current]) tickerSection.textContent = sectionNames[current];
    } else {
        ticker.classList.remove('visible');
    }
    /* Mobile jump-to-verdict button — show after scrolling, hide near verdict */
    if (jumpBtn) {
        var verdict = document.getElementById('the-tl-dr-verdict');
        var vRect = verdict ? verdict.getBoundingClientRect() : {top:9999};
        if (window.scrollY > 400 && vRect.top > window.innerHeight) {
            jumpBtn.classList.add('visible');
        } else {
            jumpBtn.classList.remove('visible');
        }
    }
}
window.addEventListener('scroll', updateTOC, { passive: true });
updateTOC();

/* Mobile TOC close on link click */
document.querySelectorAll('.toc-mobile-dropdown a').forEach(function(a) {
    a.addEventListener('click', function() {
        document.getElementById('toc-mobile').classList.remove('open');
    });
});

/* Collapsible deep-dive sections (#3 & #13) */
function toggleSection(el) {
    el.classList.toggle('open');
}

/* Filter tag jump (#1 & #6) */
function filterJump(btn) {
    document.querySelectorAll('.filter-tag').forEach(function(t){ t.classList.remove('active'); });
    btn.classList.add('active');
    var target = btn.getAttribute('data-section');
    var el = document.getElementById(target);
    if (el) {
        /* Open the parent deep-dive if collapsed */
        var dive = el.closest('.deep-dive');
        if (dive && !dive.classList.contains('open')) dive.classList.add('open');
        el.scrollIntoView({ behavior:'smooth', block:'start' });
    }
}

/* Personalization widget (#10) */
var personState = { style:null, budget:null, priority:null };
var recommendations = {
    'solo_backpacker_food': 'For a <strong>solo backpacker who cares about food</strong>, we recommend <strong>Madrid</strong>. The tapas culture is more authentic, the prices are significantly lower, and solo travelers consistently report feeling more welcome in Madrid\'s neighborhood bars.',
    'solo_backpacker_culture': 'For a <strong>solo backpacker into culture</strong>, choose <strong>Madrid</strong>. The Prado and Reina Sofia are world-class, hostels are cheaper, and the city feels genuinely local. Solo female travelers especially rate Madrid highly.',
    'solo_backpacker_beaches': 'For a <strong>solo backpacker wanting beaches</strong>, go to <strong>Barcelona</strong>. Barceloneta is 15 minutes by metro, hostels are pricier but the coast access is unbeatable. Mar Bella beach has a more local crowd.',
    'solo_backpacker_nightlife': 'For a <strong>solo backpacker chasing nightlife</strong>, both are excellent. <strong>Madrid</strong> edges it for bar-hopping with locals (Malasana is perfect). Barcelona\'s clubs are world-famous but pricier.',
    'solo_midrange_food': 'For a <strong>solo mid-range traveler who loves food</strong>, pick <strong>Madrid</strong>. Menu del dia lunches run &euro;12-14 (3 courses + wine), and the tapas crawl in La Latina is one of Europe\'s best food experiences.',
    'solo_midrange_culture': 'For a <strong>solo traveler focused on culture</strong>, <strong>Madrid</strong> is the clear winner. The Prado-Reina Sofia-Thyssen triangle is unmatched. The city is walkable, safe, and solo-friendly.',
    'solo_midrange_beaches': 'For a <strong>solo mid-range trip with beach time</strong>, <strong>Barcelona</strong> is the answer. Combine Gaudi, El Born neighborhood dining, and Barceloneta beach in one walkable city.',
    'solo_midrange_nightlife': 'For a <strong>solo mid-range traveler wanting nightlife</strong>, try <strong>Madrid</strong>. The bar scene in Chueca and Malasana is authentically Spanish, and you\'ll mix with locals more than tourists.',
    'couple_midrange_food': 'For a <strong>couple focused on food</strong>, <strong>Madrid</strong> offers the more romantic dining experience — intimate tabernas, shared plates of jamon, and incredible value. Barcelona\'s Disfrutar is world-class if you want one splurge meal.',
    'couple_midrange_beaches': 'For a <strong>couple wanting beach + city</strong>, <strong>Barcelona</strong>. El Born for evening strolls, Barceloneta at sunset, Gaudi by day. It\'s Europe\'s most photogenic city break.',
    'couple_midrange_culture': 'For a <strong>couple into culture</strong>, <strong>Madrid</strong>. The Prado alone justifies the trip, and the city\'s neighborhood character (Malasana, Chueca) creates a more intimate experience than Barcelona\'s tourist corridors.',
    'couple_midrange_nightlife': 'For a <strong>couple seeking nightlife</strong>, both work. <strong>Barcelona</strong> for a big night out at Razzmatazz. <strong>Madrid</strong> for rooftop cocktails and flamenco shows.',
    'couple_luxury_food': 'For a <strong>luxury couple focused on food</strong>, <strong>Barcelona</strong> edges it — Disfrutar (world top 5), and the Sant Antoni dining scene is extraordinary. Madrid\'s fine dining is excellent but less Michelin-dense.',
    'couple_luxury_beaches': 'For a <strong>luxury couple wanting beach access</strong>, <strong>Barcelona</strong>. The W Hotel on Barceloneta, fine dining in El Born, and Gaudi\'s masterpieces. The ultimate European city-beach luxury trip.',
    'couple_luxury_culture': 'For a <strong>luxury couple into culture</strong>, consider <strong>both</strong> — the AVE train is 2.5 hours. Prado + flamenco in Madrid, then Gaudi + Mediterranean dining in Barcelona.',
    'family_midrange_beaches': 'For a <strong>family wanting beaches</strong>, <strong>Barcelona</strong>. Barceloneta and Bogatell are kid-friendly, and Park Guell is magical for children. The city is very stroller-friendly on the Eixample grid.',
    'family_midrange_culture': 'For a <strong>family focused on culture</strong>, <strong>Madrid</strong>. Retiro Park (free rowboats, crystal palace) is perfect for kids. The Royal Palace and Prado are awe-inspiring. More affordable family dining too.',
    'family_midrange_food': 'For a <strong>family of foodies</strong>, <strong>Madrid</strong>. Kids love the churros con chocolate tradition, and the Mercado de la Paz is family-friendly. Budget goes further with menu del dia meals.',
    'friends_midrange_nightlife': 'For a <strong>friend group wanting nightlife</strong>, <strong>Barcelona</strong>. Razzmatazz and the Poble Sec bar scene are built for group nights out. Day recovery on Barceloneta beach is unbeatable.',
    'friends_backpacker_nightlife': 'For <strong>friends on a budget wanting nightlife</strong>, <strong>Madrid</strong>. Cheaper drinks, free tapas with beer at some bars, and Malasana is the perfect group bar-crawl neighborhood.',
    'friends_midrange_food': 'For a <strong>friend group focused on food</strong>, <strong>Madrid</strong>. Tapas is inherently social — sharing plates at Cava Baja is one of Europe\'s best group dining experiences.',
    'friends_midrange_beaches': 'For <strong>friends wanting beach + fun</strong>, <strong>Barcelona</strong>. Beach by day, tapas in El Born, clubs at night. It\'s the ultimate group city break in Europe.'
};

function selectPill(btn) {
    var group = btn.parentElement.getAttribute('data-group');
    btn.parentElement.querySelectorAll('.personalize-pill').forEach(function(p){ p.classList.remove('selected'); });
    btn.classList.add('selected');
    personState[group] = btn.getAttribute('data-val');
    showRecommendation();
}

function showRecommendation() {
    var s = personState;
    if (!s.style || !s.budget || !s.priority) return;
    var key = s.style + '_' + s.budget + '_' + s.priority;
    var result = document.getElementById('personalize-result');
    var text = recommendations[key];
    if (!text) {
        /* Fallback based on priority */
        var fallbacks = {
            'food': 'For <strong>food lovers</strong>, Madrid wins on tapas authenticity and value. Barcelona wins on fine dining and Catalan cuisine.',
            'culture': 'For <strong>culture seekers</strong>, Madrid\'s Prado and Reina Sofia are world-class. Barcelona\'s Gaudi architecture is unmatched.',
            'beaches': 'If <strong>beach access</strong> matters, Barcelona is the clear winner — 4.5km of coastline vs Madrid\'s 300km drive to the sea.',
            'nightlife': 'For <strong>nightlife</strong>, both are elite. Barcelona for mega-clubs, Madrid for authentic bar culture and flamenco.'
        };
        text = fallbacks[s.priority] || 'Both cities are excellent — it depends on your priorities. Scroll down to compare specific categories.';
    }
    result.innerHTML = text;
    result.classList.add('visible');
}