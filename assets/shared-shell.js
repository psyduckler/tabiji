document.addEventListener('click', function (event) {
  document.querySelectorAll('.nav-dropdown.open').forEach(function (dropdown) {
    if (!dropdown.contains(event.target)) {
      dropdown.classList.remove('open');
    }
  });
});

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js').catch(function () {});
}

/* ── Offline indicator ──────────────────────────────────── */
(function () {
  'use strict';

  var pill = null;

  function createPill() {
    if (pill) return pill;
    pill = document.createElement('a');
    pill.href = '/offline/';
    pill.className = 'offline-indicator';
    pill.textContent = 'Offline';
    pill.setAttribute('aria-label', 'You are offline — view emergency kit');

    // Insert into nav, after hamburger / before nav-links, or at end of nav
    var nav = document.querySelector('nav');
    if (!nav) return pill;

    var hamburger = nav.querySelector('.hamburger');
    if (hamburger) {
      nav.insertBefore(pill, hamburger);
    } else {
      var navLinks = nav.querySelector('.nav-links');
      if (navLinks) {
        nav.insertBefore(pill, navLinks);
      } else {
        nav.appendChild(pill);
      }
    }
    return pill;
  }

  function updateStatus() {
    var isOffline = !navigator.onLine;
    if (isOffline) {
      var el = createPill();
      // Force reflow for animation
      void el.offsetWidth;
      el.classList.add('visible');
    } else if (pill) {
      pill.classList.remove('visible');
      // Remove from DOM after animation
      setTimeout(function () {
        if (pill && !pill.classList.contains('visible')) {
          pill.style.display = 'none';
        }
      }, 350);
    }
  }

  window.addEventListener('online', updateStatus);
  window.addEventListener('offline', updateStatus);

  // Check on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateStatus);
  } else {
    updateStatus();
  }
})();
