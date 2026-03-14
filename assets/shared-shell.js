document.addEventListener('click', function (event) {
  document.querySelectorAll('.nav-dropdown.open').forEach(function (dropdown) {
    if (!dropdown.contains(event.target)) {
      dropdown.classList.remove('open');
    }
  });
});
