/* ══════════════════════════════════════════════════════════
   Compare Page UX Upgrade — Progressive Enhancement JS
   Reads existing DOM, injects interactive components.
   If anything fails, the page degrades gracefully.
   ══════════════════════════════════════════════════════════ */
(function() {
    'use strict';

    // Only run on compare pages with deep-dive sections
    var deepDives = document.querySelectorAll('section.deep-dive');
    if (!deepDives.length) return;

    // ─── Extract destination names from h1 ───
    var h1 = document.querySelector('.hero h1, h1');
    if (!h1) return;
    var h1Text = h1.textContent.trim();
    var vsMatch = h1Text.match(/^(.+?)\s+vs\.?\s+(.+?)(?:\s*[:—–\-].+)?$/i);
    if (!vsMatch) return;
    var dest1 = vsMatch[1].trim();
    var dest2 = vsMatch[2].trim();

    // ─── Extract winners from each deep-dive ───
    var sections = [];
    deepDives.forEach(function(dd) {
        var h2 = dd.querySelector('h2[id]');
        if (!h2) return;
        var id = h2.id;
        var heading = h2.textContent.trim();

        // Skip methodology/intro sections
        if (id === 'how-we-built-this-comparison' || id === 'quick-comparison') return;
        if (/methodology|how.we/i.test(heading)) return;

        // Determine winner from section-winner or tabiji-verdict
        var winner = 'tie';
        var winnerEl = dd.querySelector('.section-winner');
        var verdictEl = dd.querySelector('.tabiji-verdict');
        var sourceText = '';

        if (winnerEl) {
            sourceText = winnerEl.textContent;
        } else if (verdictEl) {
            sourceText = verdictEl.textContent;
        }

        if (sourceText) {
            var st = sourceText.toLowerCase();
            var d1l = dest1.toLowerCase();
            var d2l = dest2.toLowerCase();
            // Check for explicit "Winner: X" pattern first
            var winnerMatch = sourceText.match(/Winner:\s*(\S+)/i);
            if (winnerMatch) {
                var wt = winnerMatch[1].toLowerCase();
                if (wt.indexOf(d1l.split(' ')[0].toLowerCase()) !== -1) winner = 'd1';
                else if (wt.indexOf(d2l.split(' ')[0].toLowerCase()) !== -1) winner = 'd2';
                else if (/tie|draw|both/i.test(wt)) winner = 'tie';
            }
            // Fallback: look for "X wins" / "X is better" etc.
            if (winner === 'tie' && !winnerMatch) {
                if (new RegExp(d1l + '\\s+(wins|edges?|is (safer|cheaper|better|stronger))', 'i').test(st)) winner = 'd1';
                else if (new RegExp(d2l + '\\s+(wins|edges?|is (safer|cheaper|better|stronger))', 'i').test(st)) winner = 'd2';
                // Check for "X wins" at word boundary with first word of dest name
                else if (new RegExp(d1l.split(' ')[0] + '\\s+wins', 'i').test(st)) winner = 'd1';
                else if (new RegExp(d2l.split(' ')[0] + '\\s+wins', 'i').test(st)) winner = 'd2';
            }
        }

        sections.push({ el: dd, id: id, heading: heading, winner: winner });
    });

    if (!sections.length) return;

    // Count scores
    var d1Wins = 0, d2Wins = 0, ties = 0;
    sections.forEach(function(s) {
        if (s.winner === 'd1') d1Wins++;
        else if (s.winner === 'd2') d2Wins++;
        else ties++;
    });

    // ─── 1. Score Ticker (skip if page already has one) ───
    if (!document.getElementById('score-ticker') && !document.getElementById('ux-ticker')) {
    var ticker = document.createElement('div');
    ticker.className = 'ux-ticker';
    ticker.id = 'ux-ticker';
    ticker.innerHTML = '<span class="t-d1">' + dest1 + ' ' + d1Wins + '</span><span class="t-sep">&mdash;</span><span class="t-d2">' + d2Wins + ' ' + dest2 + '</span><span class="t-sep">|</span><span class="t-section" id="ux-ticker-section">' + ties + ' ties</span>';
    var nav = document.querySelector('nav');
    if (nav && nav.nextSibling) {
        nav.parentNode.insertBefore(ticker, nav.nextSibling);
    }
    }

    // ─── 2. Filter Tags ───
    var iconMap = {
        'budget':'💰','cost':'💰','value':'💰','price':'💰',
        'food':'🍽','dining':'🍽','drink':'🍷','cuisine':'🍽',
        'beach':'🏖','water':'🏖','coast':'🏖','island':'🏖',
        'nightlife':'🎉','entertainment':'🎉','party':'🎉',
        'culture':'🏛','architecture':'🏛','history':'🏛','art':'🏛','museum':'🏛',
        'safety':'🛡','security':'🛡',
        'transport':'🚇','getting':'🚇',
        'nature':'⛰','scenery':'⛰','outdoor':'⛰','hiking':'⛰',
        'weather':'🌤','climate':'🌤','time':'🌤','season':'🌤',
        'accommodation':'🏨','stay':'🏨','neighborhood':'🏘',
        'day trip':'🗺','excursion':'🗺',
        'solo':'🚶','vibe':'🏙','character':'🏙','atmosphere':'🏙'
    };
    function getIcon(heading) {
        var hl = heading.toLowerCase();
        for (var kw in iconMap) { if (hl.indexOf(kw) !== -1) return iconMap[kw]; }
        return '📌';
    }
    function getShortLabel(heading) {
        // Strip leading emoji
        var label = heading.replace(/^[\u{1F000}-\u{1FFFF}\u{2600}-\u{27FF}\u{FE00}-\u{FE0F}\u{200D}\u{20E3}\u{E0020}-\u{E007F}]+\s*/u, '').replace(/&amp;/g, '&');
        if (label.length > 16) label = label.split(/\s+/).slice(0, 2).join(' ');
        return label;
    }

    var hero = document.querySelector('.hero');
    if (hero && !document.querySelector('.ux-filters, .priority-filter')) {
        var filtersDiv = document.createElement('div');
        filtersDiv.className = 'ux-filters';
        filtersDiv.innerHTML = '<p class="ux-filters-label">What matters most to you?</p><div class="ux-filters-row"></div>';
        var row = filtersDiv.querySelector('.ux-filters-row');
        sections.slice(0, 8).forEach(function(s) {
            var btn = document.createElement('button');
            btn.className = 'ux-filter-tag';
            btn.textContent = getIcon(s.heading) + ' ' + getShortLabel(s.heading);
            btn.addEventListener('click', function() {
                document.querySelectorAll('.ux-filter-tag').forEach(function(t) { t.classList.remove('active'); });
                this.classList.add('active');
                // Open the section if collapsed
                if (!s.el.classList.contains('ux-open')) s.el.classList.add('ux-open');
                s.el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            });
            row.appendChild(btn);
        });
        hero.parentNode.insertBefore(filtersDiv, hero.nextSibling);
    }

    // ─── 3. Quick Answers (skip if page already has them) ───
    var compTable = document.querySelector('.comparison-table');
    var verdictBox = document.querySelector('.verdict-box');
    if (compTable && verdictBox && !document.querySelector('.ux-quick-answers, .quick-answers')) {
        var qaDiv = document.createElement('div');
        qaDiv.className = 'ux-quick-answers';
        qaDiv.innerHTML = '<h2>⚡ Quick Answers</h2><div class="ux-qa-grid"></div>';
        var qaGrid = qaDiv.querySelector('.ux-qa-grid');

        // Build from comparison table rows
        var rows = compTable.querySelectorAll('tbody tr');
        var qaCount = 0;
        rows.forEach(function(tr) {
            if (qaCount >= 6) return;
            var cells = tr.querySelectorAll('td');
            if (cells.length < 3) return;
            var category = cells[0].textContent.trim();
            var val1 = cells[1].textContent.trim();
            var val2 = cells[2].textContent.trim();
            var winnerCell = cells[3] ? cells[3].textContent.trim() : '';

            // Determine badge
            var badgeClass = 'tie', badgeText = 'Tie';
            if (winnerCell.toLowerCase().indexOf(dest1.toLowerCase().split(' ')[0].toLowerCase()) !== -1) {
                badgeClass = 'd1'; badgeText = dest1 + ' wins';
            } else if (winnerCell.toLowerCase().indexOf(dest2.toLowerCase().split(' ')[0].toLowerCase()) !== -1) {
                badgeClass = 'd2'; badgeText = dest2 + ' wins';
            }

            var card = document.createElement('a');
            card.className = 'ux-qa-card';
            card.href = '#' + (sections.length > qaCount ? sections[qaCount].id : '');
            card.innerHTML = '<div class="qa-q">Which is better for ' + category.toLowerCase().replace(/\s*\(.*?\)/, '') + '?</div>' +
                '<div class="qa-a">' + dest1 + ': ' + val1.substring(0, 60) + (val1.length > 60 ? '...' : '') + '<br>' + dest2 + ': ' + val2.substring(0, 60) + (val2.length > 60 ? '...' : '') + '</div>' +
                '<span class="qa-badge ' + badgeClass + '">' + badgeText + '</span>';
            qaGrid.appendChild(card);
            qaCount++;
        });

        if (qaCount > 0) {
            verdictBox.parentNode.insertBefore(qaDiv, verdictBox);
        }
    }

    // ─── 4. Visual Scorecard (skip if page already has one) ───
    var compSection = document.querySelector('.comparison-section');
    if (compSection && !document.querySelector('.ux-scorecard, .scorecard')) {
        var scDiv = document.createElement('div');
        scDiv.className = 'ux-scorecard';
        var scRows = '';
        sections.forEach(function(s) {
            var d1Pct, d2Pct, winnerHtml;
            if (s.winner === 'd1') {
                d1Pct = 85; d2Pct = 50;
                winnerHtml = '<span class="ux-sc-winner d1">' + dest1 + '</span>';
            } else if (s.winner === 'd2') {
                d1Pct = 50; d2Pct = 85;
                winnerHtml = '<span class="ux-sc-winner d2">' + dest2 + '</span>';
            } else {
                d1Pct = 72; d2Pct = 72;
                winnerHtml = '<span class="ux-sc-winner tie">Tie</span>';
            }
            scRows += '<a class="ux-sc-row" href="#' + s.id + '">' +
                '<span class="sc-label">' + getIcon(s.heading) + ' ' + getShortLabel(s.heading) + '</span>' +
                '<span class="ux-sc-bars"><span class="ux-sc-bar-wrap"><span class="ux-sc-bar d1" style="width:' + d1Pct + '%"></span></span>' +
                '<span class="ux-sc-bar-wrap"><span class="ux-sc-bar d2" style="width:' + d2Pct + '%"></span></span></span>' +
                winnerHtml + '</a>';
        });

        scDiv.innerHTML = '<h2>📊 Visual Scorecard</h2>' +
            '<div class="ux-sc-overall">' +
            '<div class="ux-sc-city d1"><div class="c-name">' + dest1.toUpperCase() + '</div><div class="c-score">' + d1Wins + '</div></div>' +
            '<div class="ux-sc-vs">vs</div>' +
            '<div class="ux-sc-city d2"><div class="c-name">' + dest2.toUpperCase() + '</div><div class="c-score">' + d2Wins + '</div></div>' +
            '</div>' +
            '<div class="ux-sc-rows">' + scRows + '</div>';

        compSection.parentNode.insertBefore(scDiv, compSection.nextSibling);
    }

    // ─── 5. Collapsible Deep Dives ───
    // Skip if page already has its own collapsible structure (e.g. madrid-vs-barcelona manual rewrite)
    var alreadyCollapsible = document.querySelector('.dd-header');
    if (alreadyCollapsible) {
        // Just wire up existing dd-header click handlers if not already wired
        document.querySelectorAll('.dd-header').forEach(function(h) {
            h.style.cursor = 'pointer';
            h.addEventListener('click', function() { this.parentElement.classList.toggle('open'); });
        });
    }

    if (!alreadyCollapsible) sections.forEach(function(s, i) {
        var dd = s.el;
        var h2 = dd.querySelector('h2[id]');
        if (!h2) return;

        // Create the clickable bar
        var bar = document.createElement('div');
        bar.className = 'ux-dd-bar';

        // Badge
        var badgeClass = s.winner === 'd1' ? 'd1' : s.winner === 'd2' ? 'd2' : 'tie';
        var badgeText = s.winner === 'd1' ? dest1 + ' wins' : s.winner === 'd2' ? dest2 + ' wins' : 'Tie';

        var meta = document.createElement('div');
        meta.className = 'ux-dd-meta';
        meta.innerHTML = '<span class="ux-dd-badge ' + badgeClass + '">' + badgeText + '</span><span class="ux-dd-arrow">▾</span>';

        // Move h2 into bar
        bar.appendChild(h2);
        bar.appendChild(meta);

        // Wrap remaining content
        var body = document.createElement('div');
        body.className = 'ux-dd-body';
        while (dd.children.length > 0 && dd.children[0] !== bar) {
            // Move first child if it's not our bar
            if (dd.firstChild === bar) break;
            body.appendChild(dd.firstChild);
        }
        // Move everything after bar into body
        while (bar.nextSibling) {
            body.appendChild(bar.nextSibling);
        }

        dd.innerHTML = '';
        dd.appendChild(bar);
        dd.appendChild(body);

        // First 2 sections open by default
        if (i < 2) dd.classList.add('ux-open');

        bar.addEventListener('click', function() {
            dd.classList.toggle('ux-open');
        });
    });

    // ─── 6. Jump to Verdict (mobile) ───
    var jumpBtn = document.createElement('button');
    jumpBtn.className = 'ux-jump';
    jumpBtn.id = 'ux-jump';
    jumpBtn.textContent = '⚡ Jump to Verdict';
    jumpBtn.addEventListener('click', function() {
        var v = document.getElementById('the-tl-dr-verdict');
        if (v) v.scrollIntoView({ behavior: 'smooth' });
    });
    document.body.appendChild(jumpBtn);

    // ─── 7. Scroll tracking: ticker + jump button ───
    var tickerEl = document.getElementById('ux-ticker');
    var tickerSec = document.getElementById('ux-ticker-section');
    var jumpEl = document.getElementById('ux-jump');
    var allIds = document.querySelectorAll('[id]');

    var sectionNameMap = {};
    sections.forEach(function(s) { sectionNameMap[s.id] = getShortLabel(s.heading); });
    sectionNameMap['the-tl-dr-verdict'] = 'Verdict';
    sectionNameMap['quick-comparison'] = 'Comparison';
    sectionNameMap['the-decision-framework'] = 'Decision';
    sectionNameMap['frequently-asked-questions'] = 'FAQ';

    function onScroll() {
        var current = '';
        allIds.forEach(function(el) {
            if (el.getBoundingClientRect().top <= 120) current = el.id;
        });

        // Ticker
        if (tickerEl && hero) {
            if (hero.getBoundingClientRect().bottom < 0) {
                tickerEl.classList.add('visible');
                if (sectionNameMap[current]) tickerSec.textContent = sectionNameMap[current];
            } else {
                tickerEl.classList.remove('visible');
            }
        }

        // Jump button
        if (jumpEl) {
            var verdict = document.getElementById('the-tl-dr-verdict');
            var vTop = verdict ? verdict.getBoundingClientRect().top : 9999;
            if (window.scrollY > 400 && vTop > window.innerHeight) {
                jumpEl.classList.add('visible');
            } else {
                jumpEl.classList.remove('visible');
            }
        }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // ─── 8. Remove duplicate decision frameworks ───
    var decisionSections = document.querySelectorAll('section.deep-dive');
    var decisionCount = 0;
    decisionSections.forEach(function(dd) {
        var h = dd.querySelector('h2');
        if (h && /decision.framework/i.test(h.textContent)) {
            decisionCount++;
            if (decisionCount > 1) dd.style.display = 'none';
        }
    });

    // ─── 9. Remove sports quotes ───
    document.querySelectorAll('.reddit-quote, blockquote.reddit-quote').forEach(function(q) {
        var t = q.textContent;
        if (/Goal!|⚽|\d+['′]\s|match thread|half.time|full.time/i.test(t)) {
            q.style.display = 'none';
        }
    });

})();
