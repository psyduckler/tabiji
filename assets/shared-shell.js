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
