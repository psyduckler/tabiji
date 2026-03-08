#!/bin/bash
# Add Export to Google Docs button to all /i/ pages that don't have it yet
set -e

EXPORT_API='https://script.google.com/macros/s/AKfycbwisEgM3k14bSlEYY-YuNaHSqEIhOdjwfZmJ5o1RxnuCY90943fXtYYpQaziCDG56AE/exec'

CSS_BLOCK='        .export-nav { display:inline-flex;align-items:center;gap:0.4rem;color:var(--indigo);text-decoration:none;font-size:0.9rem;font-weight:500;padding:0.5rem 0.8rem;border-radius:8px;transition:background 0.2s;cursor:pointer;border:none;background:none;font-family:inherit; }
        .export-nav:hover { background:var(--sand); }
        .export-nav svg { width:16px;height:16px; }
        .export-modal-overlay { display:none;position:fixed;inset:0;z-index:1000;background:rgba(0,0,0,0.5);backdrop-filter:blur(4px);justify-content:center;align-items:center;opacity:0;transition:opacity 0.2s; }
        .export-modal-overlay.active { display:flex;opacity:1; }
        .export-modal { background:var(--white);border-radius:16px;padding:2rem;max-width:420px;width:90%;box-shadow:0 20px 60px rgba(0,0,0,0.2);transform:translateY(10px);transition:transform 0.2s;text-align:center;position:relative; }
        .export-modal-overlay.active .export-modal { transform:translateY(0); }
        .export-modal h3 { font-size:1.3rem;color:var(--indigo);margin-bottom:0.5rem; }
        .export-modal p { color:var(--text-muted);font-size:0.9rem;margin-bottom:1.2rem;line-height:1.5; }
        .export-modal input[type="email"] { width:100%;padding:0.75rem 1rem;border:2px solid var(--sand);border-radius:10px;font-size:1rem;font-family:inherit;outline:none;transition:border-color 0.2s;background:var(--white);color:var(--text);box-sizing:border-box; }
        .export-modal input[type="email"]:focus { border-color:var(--indigo); }
        .export-submit { width:100%;padding:0.75rem;margin-top:0.8rem;background:var(--indigo);color:var(--warm-cream);border:none;border-radius:10px;font-size:1rem;font-weight:600;cursor:pointer;font-family:inherit;transition:background 0.2s; }
        .export-submit:hover:not(:disabled) { background:var(--indigo-light); }
        .export-submit:disabled { opacity:0.6;cursor:wait; }
        .export-close { position:absolute;top:0.8rem;right:1rem;background:none;border:none;font-size:1.5rem;color:var(--text-muted);cursor:pointer; }
        .export-error { color:var(--terracotta);font-size:0.85rem;margin-top:0.5rem;display:none; }
        .export-success { display:none; }
        .export-success.show { display:block; }
        .export-success a { display:inline-block;margin-top:1rem;padding:0.6rem 1.5rem;background:var(--indigo);color:var(--warm-cream);border-radius:10px;text-decoration:none;font-weight:600; }
        .export-form { display:block; }
        .export-form.hide { display:none; }'

NAV_BUTTON='        <button class="export-nav" onclick="openExportModal()" title="Export to Google Docs">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
          <span>Google Docs</span>
        </button>'

count=0
skipped=0

for page in ~/tabiji/i/*/index.html; do
    # Skip if already has export button
    if grep -q "export-nav" "$page" 2>/dev/null; then
        skipped=$((skipped + 1))
        continue
    fi
    
    # 1. Add CSS before the .hamburger style (or after cta-nav:hover)
    if grep -q "nav a.cta-nav:hover" "$page"; then
        sed -i '' "/nav a.cta-nav:hover.*{.*}/a\\
${CSS_BLOCK}
" "$page"
    fi
    
    # 2. Add nav button before the CTA link
    sed -i '' 's|<div class="nav-links">|<div class="nav-links">\
'"${NAV_BUTTON}"'|' "$page"
    
    # 3. Add modal + JS before </body>
    sed -i '' '/<\/body>/i\
<div class="export-modal-overlay" id="exportModal" onclick="if(event.target===this)closeExportModal()">\
  <div class="export-modal">\
    <button class="export-close" onclick="closeExportModal()" aria-label="Close">\&times;</button>\
    <div class="export-form" id="exportForm">\
      <h3>📄 Export to Google Docs</h3>\
      <p>Get an editable Google Doc of this itinerary — perfect for sharing with your travel group and adding your own notes.</p>\
      <input type="email" id="exportEmail" placeholder="your@email.com" autocomplete="email" />\
      <div class="export-error" id="exportError"></div>\
      <button class="export-submit" id="exportSubmit" onclick="submitExport()">Create My Google Doc</button>\
      <p style="font-size:0.75rem;color:var(--text-muted);margin-top:0.6rem;margin-bottom:0;">The doc will be shared to your email as an editor.</p>\
    </div>\
    <div class="export-success" id="exportSuccess">\
      <h3>✅ Your Google Doc is ready!</h3>\
      <p>We'"'"'ve shared it with <strong id="exportEmailConfirm"></strong>. Check your Google Drive or click below.</p>\
      <a id="exportDocLink" href="#" target="_blank" rel="noopener">Open Google Doc →</a>\
      <p style="font-size:0.75rem;color:var(--text-muted);margin-top:1rem;margin-bottom:0;">Tip: You can edit, add notes, and share it with your travel group!</p>\
    </div>\
  </div>\
</div>\
<script>\
var EXPORT_API='"'"''"$EXPORT_API"''"'"';\
function getSlug(){var m=window.location.pathname.match(/\\/i\\/([^\\/]+)/);return m?m[1]:'"'"''"'"';}\
function openExportModal(){document.getElementById('"'"'exportModal'"'"').classList.add('"'"'active'"'"');document.getElementById('"'"'exportEmail'"'"').focus();document.getElementById('"'"'exportForm'"'"').classList.remove('"'"'hide'"'"');document.getElementById('"'"'exportSuccess'"'"').classList.remove('"'"'show'"'"');document.getElementById('"'"'exportError'"'"').style.display='"'"'none'"'"';document.getElementById('"'"'exportSubmit'"'"').disabled=false;document.getElementById('"'"'exportSubmit'"'"').textContent='"'"'Create My Google Doc'"'"';}\
function closeExportModal(){document.getElementById('"'"'exportModal'"'"').classList.remove('"'"'active'"'"');}\
function submitExport(){var email=document.getElementById('"'"'exportEmail'"'"').value.trim();var slug=getSlug();var err=document.getElementById('"'"'exportError'"'"');var btn=document.getElementById('"'"'exportSubmit'"'"');if(!email||!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)){err.textContent='"'"'Please enter a valid email address.'"'"';err.style.display='"'"'block'"'"';return;}if(!slug){err.textContent='"'"'Could not detect itinerary.'"'"';err.style.display='"'"'block'"'"';return;}err.style.display='"'"'none'"'"';btn.disabled=true;btn.textContent='"'"'Creating your doc...'"'"';fetch(EXPORT_API,{method:'"'"'POST'"'"',redirect:'"'"'follow'"'"',headers:{'"'"'Content-Type'"'"':'"'"'text/plain'"'"'},body:JSON.stringify({slug:slug,email:email})}).then(function(r){return r.json();}).then(function(data){if(data.error){err.textContent=data.error;err.style.display='"'"'block'"'"';btn.disabled=false;btn.textContent='"'"'Create My Google Doc'"'"';return;}document.getElementById('"'"'exportForm'"'"').classList.add('"'"'hide'"'"');document.getElementById('"'"'exportSuccess'"'"').classList.add('"'"'show'"'"');document.getElementById('"'"'exportEmailConfirm'"'"').textContent=email;document.getElementById('"'"'exportDocLink'"'"').href=data.docUrl;if(typeof gtag==='"'"'function'"'"')gtag('"'"'event'"'"','"'"'export_google_doc'"'"',{event_category:'"'"'engagement'"'"',event_label:slug,value:1});}).catch(function(){err.textContent='"'"'Something went wrong. Please try again.'"'"';err.style.display='"'"'block'"'"';btn.disabled=false;btn.textContent='"'"'Create My Google Doc'"'"';});}\
document.addEventListener('"'"'keydown'"'"',function(e){if(e.key==='"'"'Escape'"'"')closeExportModal();});\
</script>
' "$page"
    
    count=$((count + 1))
done

echo "✅ Updated: $count pages"
echo "⏭️ Skipped (already had it): $skipped"
