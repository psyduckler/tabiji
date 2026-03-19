# TikTok API Demo Video — Screen Recording Script (v2)

**Dashboard URL:** https://tabiji.ai/media/dashboard/
**Duration:** ~90 seconds
**Resolution:** 1280x800 or higher
**IMPORTANT:** Use a TikTok sandbox test user, NOT a production account

## Recording Flow

### Scene 1: Dashboard Overview (5s)
- Open `https://tabiji.ai/media/dashboard/`
- Show the dashboard home with stat cards and recent videos

### Scene 2: Connected Accounts — TikTok Not Connected (5s)
- Click **Connected Accounts** in sidebar
- Show TikTok as **"Not connected"** with "Connect TikTok" button
- This proves the app starts without any hardcoded connections

### Scene 3: TikTok Login Kit — OAuth Flow (15s)
- Click **"Connect TikTok"** button
- OAuth modal appears showing:
  - Real TikTok auth URL
  - Permissions: video.publish, video.upload, user.info.basic
- Click **"Continue with TikTok"**
- **Browser redirects to TikTok's real OAuth page** (https://www.tiktok.com/v2/auth/authorize/...)
- Log in with your **sandbox test user**
- Authorize the app (grant all requested scopes)
- TikTok redirects back to `https://tabiji.ai/media/dashboard/callback`
- Callback page shows "Exchanging authorization code..." → "✅ Connected successfully!"
- Click "Go to Dashboard"

### Scene 4: Verify Connection — user.info.basic (5s)
- Navigate to **Connected Accounts**
- TikTok now shows **"● Connected (Live)"** with the sandbox user's actual username
- This demonstrates the `user.info.basic` scope (fetched real profile data)

### Scene 5: Publish Video — video.publish (15s)
- Click **Videos** in sidebar
- Click on a video with "Ready" status (e.g., "Budget Guide: Bangkok")
- Modal opens with title, description, tags
- Ensure TikTok is checked in the platform list
- Click **"Publish Now"**
- Button shows loading → makes real API call to TikTok's `/v2/post/publish/video/init/`
- Shows success (or expected sandbox restriction message)
- This demonstrates the `video.publish` scope

### Scene 6: Save as Draft — video.upload (10s)
- Open another video (e.g., "Santorini at Golden Hour")
- Click **"📥 Save as Draft"** button
- Button shows loading → makes real API call to TikTok's `/v2/post/publish/inbox/video/init/`
- Shows "✅ Sent to Drafts! Open TikTok to edit and post."
- This demonstrates the `video.upload` scope

### Scene 7: Landing Page — ToS & Privacy (5s)
- Navigate to `https://tabiji.ai/media/`
- Show the page title: "Tabiji Media Studio"
- Scroll to show the **prominent ToS & Privacy Policy links** bar
- Scroll to footer showing ToS & Privacy links again

### End

## Key Points for TikTok Reviewer
1. **Real OAuth** — Browser actually redirects to TikTok's auth page, not simulated
2. **Sandbox environment** — Using sandbox test user as required
3. **All 3 scopes demonstrated:**
   - `user.info.basic` → real username displayed after OAuth
   - `video.publish` → Publish Now button calls Direct Post API
   - `video.upload` → Save as Draft button calls Inbox Upload API
4. **Server-side token exchange** — client_secret never exposed to frontend
5. **App name matches** — "Tabiji Media Studio" on both the TikTok app and the website
6. **ToS & Privacy Policy** — prominently displayed on the website
7. **Domain matches** — all actions happen on tabiji.ai, matching the Web/Desktop URL
