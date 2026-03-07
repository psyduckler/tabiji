# Tabiji — Export to Google Docs

Lets visitors export any `/i/` itinerary page to an editable Google Doc.

## Architecture

```
User clicks "Google Docs" in nav
  → Modal asks for email
  → POST to Google Apps Script web app
  → Apps Script fetches itinerary HTML from tabiji.ai
  → Parses it → creates formatted Google Doc
  → Shares as editor with user's email
  → Returns doc URL
  → Modal shows success + link
```

## Setup (one-time)

### 1. Create the Apps Script project

1. Go to [script.google.com](https://script.google.com) → **New project**
2. Name it: `Tabiji Export to Google Docs`
3. Delete the default `Code.gs` content
4. Paste the contents of `Code.gs` from this folder
5. Click **Save** (Ctrl+S)

### 2. Deploy as web app

1. Click **Deploy** → **New deployment**
2. Click the gear icon → **Web app**
3. Settings:
   - Description: `Tabiji Export to Google Docs`
   - Execute as: **Me** (your Google account)
   - Who has access: **Anyone**
4. Click **Deploy**
5. Authorize the app when prompted (it needs Docs + Drive access)
6. **Copy the web app URL** — it looks like:
   `https://script.google.com/macros/s/AKfycb.../exec`

### 3. Test it

1. In the Apps Script editor, select `testExport` from the function dropdown
2. Click **Run** — check the Execution Log for the doc URL
3. Verify the doc was created and shared with your email

### 4. Add to itinerary pages

In the itinerary HTML template, add three things:

**a) CSS** — add the `<style>` block from `export-button.html` inside the existing `<style>` tag

**b) Nav button** — add inside `.nav-links`, before the CTA:
```html
<div class="nav-links">
    <button class="export-nav" onclick="openExportModal()" title="Export to Google Docs">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
        <polyline points="14 2 14 8 20 8"/>
        <line x1="16" y1="13" x2="8" y2="13"/>
        <line x1="16" y1="17" x2="8" y2="17"/>
        <polyline points="10 9 9 9 8 9"/>
      </svg>
      <span>Google Docs</span>
    </button>
    <a href="/plan" class="cta-nav">Get Your Itinerary</a>
</div>
```

**c) Modal + JS** — add the modal HTML and `<script>` block before `</body>`

**d) Update the API URL** — replace `YOUR_APPS_SCRIPT_WEB_APP_URL` in the script with your actual deployed URL.

## Files

| File | Purpose |
|------|---------|
| `Code.gs` | Apps Script backend — parser + doc creator |
| `export-button.html` | Frontend — CSS, button, modal, JS |
| `README.md` | This file |
