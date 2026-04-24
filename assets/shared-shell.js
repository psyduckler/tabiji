document.addEventListener('click', function (event) {
  document.querySelectorAll('.nav-dropdown.open').forEach(function (dropdown) {
    if (!dropdown.contains(event.target)) {
      dropdown.classList.remove('open');
    }
  });
});

/* ── Scam-page TOC scrollspy (editorial-v2 only) ──────────
   Highlights the current scam in the sticky TOC as the user reads. */
(function () {
  'use strict';
  function init() {
    if (!document.body.classList.contains('editorial-v2')) return;
    var tocItems = document.querySelectorAll('.toc-list li');
    if (!tocItems.length) return;

    var anchorMap = {};
    tocItems.forEach(function (li) {
      var a = li.querySelector('a[href^="#"]');
      if (!a) return;
      var id = a.getAttribute('href').slice(1);
      anchorMap[id] = li;
    });

    var targets = Object.keys(anchorMap)
      .map(function (id) { return document.getElementById(id); })
      .filter(Boolean);
    if (!targets.length) return;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          Object.keys(anchorMap).forEach(function (id) {
            anchorMap[id].classList.toggle('active', id === entry.target.id);
          });
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px', threshold: 0 });

    targets.forEach(function (t) { observer.observe(t); });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

/* ── Page breadcrumbs — render visible breadcrumbs from BreadcrumbList JSON-LD ── */
(function () {
  'use strict';
  function render() {
    if (document.querySelector('.page-breadcrumbs')) return; // already rendered
    var main = document.getElementById('main') || document.querySelector('main');
    if (!main) return;
    var scripts = document.querySelectorAll('script[type="application/ld+json"]');
    var crumbs = null;
    for (var i = 0; i < scripts.length; i++) {
      try {
        var data = JSON.parse(scripts[i].textContent);
        var blocks = Array.isArray(data) ? data : [data];
        for (var j = 0; j < blocks.length; j++) {
          var b = blocks[j];
          if (b && b['@type'] === 'BreadcrumbList' && Array.isArray(b.itemListElement)) {
            crumbs = b.itemListElement.slice().sort(function (a, c) {
              return (a.position || 0) - (c.position || 0);
            });
            break;
          }
        }
      } catch (e) { /* ignore bad JSON */ }
      if (crumbs) break;
    }
    if (!crumbs || crumbs.length < 2) return;

    var nav = document.createElement('nav');
    nav.className = 'page-breadcrumbs';
    nav.setAttribute('aria-label', 'Breadcrumb');
    var ol = document.createElement('ol');
    crumbs.forEach(function (c, idx) {
      var li = document.createElement('li');
      var isLast = idx === crumbs.length - 1;
      if (isLast) {
        li.setAttribute('aria-current', 'page');
        li.textContent = c.name || '';
      } else {
        var a = document.createElement('a');
        a.href = c.item || '#';
        a.textContent = c.name || '';
        li.appendChild(a);
      }
      ol.appendChild(li);
    });
    nav.appendChild(ol);

    // Place breadcrumbs immediately before the hero so they sit between the
    // fixed site nav and the hero on every layout (compare, popular-picks
    // hub/leaf, scams leaf). Fall back to the top of <main> when no hero
    // is present.
    var hero = document.querySelector('section.hero, header.hero, .hero');
    if (hero && hero.parentNode) {
      hero.parentNode.insertBefore(nav, hero);
    } else {
      main.insertBefore(nav, main.firstChild);
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', render);
  } else {
    render();
  }
})();
