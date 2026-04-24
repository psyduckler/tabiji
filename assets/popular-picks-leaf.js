(function () {
      var sections = Array.prototype.slice.call(document.querySelectorAll('.restaurant-section'));
      var panels = Array.prototype.slice.call(document.querySelectorAll('[data-map-panel]'));
      var mapConfig = window.__POPULAR_PICKS_MAP__ || {};
      var mapState = { maps: [] };
      if (!sections.length || !panels.length) return;
      function findPickBySection(section) {
        var id = section && section.id;
        if (!id || !Array.isArray(mapConfig.picks)) return null;
        return mapConfig.picks.find(function (pick) { return pick.anchorId === id; }) || null;
      }
      function syncPanels(section, pick) {
        panels.forEach(function (panel) {
          var title = panel.querySelector('[data-map-active-pick]');
          var cta = panel.querySelector('[data-map-cta]');
          if (title) title.textContent = (section && section.dataset.mapName) || (pick && pick.label) || '';
          if (cta) cta.href = (pick && pick.ctaUrl) || (section && section.dataset.mapCtaUrl) || mapConfig.defaultCtaUrl || '#';
        });
      }
      function highlightMarker(activePick) {
        mapState.maps.forEach(function (entry) {
          entry.markers.forEach(function (markerEntry) {
            var isActive = activePick && markerEntry.pick.anchorId === activePick.anchorId;
            markerEntry.marker.setIcon({ path: google.maps.SymbolPath.CIRCLE, scale: isActive ? 12 : 9, fillColor: isActive ? '#2D3A5C' : '#A85A37', fillOpacity: 1, strokeColor: '#FFFFFF', strokeWeight: 2 });
            markerEntry.marker.setZIndex(isActive ? 1000 : markerEntry.pick.rank);
          });
          if (activePick) entry.map.panTo({ lat: activePick.lat, lng: activePick.lng });
        });
      }
      function setActive(section) {
        if (!section) return;
        var activePick = findPickBySection(section);
        sections.forEach(function (item) { item.classList.toggle('active', item === section); });
        syncPanels(section, activePick);
        if (window.google && google.maps && activePick) highlightMarker(activePick);
      }
      function initMaps() {
        if (!mapConfig.enabled || !Array.isArray(mapConfig.picks) || !mapConfig.picks.length) return;
        panels.forEach(function (panel) {
          var canvas = panel.querySelector('[data-map-canvas]');
          if (!canvas) return;
          var map = new google.maps.Map(canvas, { center: { lat: mapConfig.picks[0].lat, lng: mapConfig.picks[0].lng }, zoom: 13, mapTypeControl: false, streetViewControl: false, fullscreenControl: false, clickableIcons: false, styles: [{ featureType: 'poi', stylers: [{ visibility: 'off' }] }, { featureType: 'transit', stylers: [{ visibility: 'off' }] }] });
          var bounds = new google.maps.LatLngBounds();
          var markers = mapConfig.picks.map(function (pick) {
            var marker = new google.maps.Marker({ position: { lat: pick.lat, lng: pick.lng }, map: map, title: pick.label, label: { text: String(pick.rank), color: '#FFFFFF', fontWeight: '700' } });
            var infoWindow = new google.maps.InfoWindow({ content: '<strong>' + pick.label.replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</strong>' });
            marker.addListener('click', function () { infoWindow.open({ anchor: marker, map: map }); var target = document.getElementById(pick.anchorId); if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
            bounds.extend(marker.getPosition());
            return { pick: pick, marker: marker, infoWindow: infoWindow };
          });
          if (mapConfig.picks.length > 1) map.fitBounds(bounds, 48);
          mapState.maps.push({ panel: panel, map: map, markers: markers });
        });
        setTimeout(function () { setActive(sections[0]); }, 0);
      }
      window.initPopularPicksMaps = initMaps;
      setActive(sections[0]);
      if ('IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function (entries) {
          var visible = entries.filter(function (entry) { return entry.isIntersecting; }).sort(function (a, b) { return b.intersectionRatio - a.intersectionRatio; });
          if (visible[0]) setActive(visible[0].target);
        }, { rootMargin: '-25% 0px -45% 0px', threshold: [0.2, 0.45, 0.7] });
        sections.forEach(function (section) { observer.observe(section); });
      }
    }());
