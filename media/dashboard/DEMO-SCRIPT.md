# TikTok API Demo Video — Screen Recording Script (v3)

**Dashboard URL:** https://tabiji.ai/media/dashboard/
**Duration:** ~2 minutes
**Resolution:** 1280x800 or higher
**IMPORTANT:** Use a TikTok sandbox test user, NOT a production account

> This script follows TikTok's Content Sharing Developer Guidelines **Points 1-5 in order**, as required by the reviewer feedback.

## Recording Flow

### Scene 1: Dashboard Overview (5s)
- Open `https://tabiji.ai/media/dashboard/`
- Show the dashboard home with stat cards and recent videos

### Scene 2: Connected Accounts — TikTok Not Connected (5s)
- Click **Connected Accounts** in sidebar
- Show TikTok as **"Not connected"** with "Connect TikTok" button

### Scene 3: TikTok Login Kit — OAuth Flow (15s)
- Click **"Connect TikTok"**
- OAuth modal appears showing real TikTok auth URL and requested permissions
- Click **"Continue with TikTok"**
- Browser redirects to TikTok's real OAuth page
- Log in with **sandbox test user** and authorize
- Callback page shows success, click "Go to Dashboard"

### Scene 4: Point 1 — Creator Info Display (5s)
- Navigate to **Connected Accounts**
- TikTok now shows **"Connected (Live)"** with the sandbox user's actual username
- This demonstrates `user.info.basic` scope and creator info retrieval

### Scene 5: Open a Video for Publishing (5s)
- Click **Videos** in sidebar
- Click on a video with "Ready" status (e.g., "Budget Guide: Bangkok")
- Publish modal opens — TikTok is selected, **TikTok Post Settings panel** is visible
- **Point 1:** Show the creator's nickname displayed at the top of settings

### Scene 6: Point 2 — Privacy & Interaction Settings (15s)
- **Privacy Level dropdown**: Click to show it has NO default selected
  - Show the available options (Public, Friends only, Only me)
  - Select **"Public"**
- **Interaction Settings**: Show all three checkboxes are UNCHECKED by default
  - Check **"Allow Comments"**
  - Check **"Allow Duets"**
  - Leave **"Allow Stitches"** unchecked to show user has control
- Pause briefly so reviewer can see the full interaction between privacy and interaction settings

### Scene 7: Point 3 — Commercial Content Disclosure (15s)
- Show the **Music Usage Confirmation** consent line at the top of the section
- Click the **commercial content toggle** to enable it
- Show the two options appear:
  - Check **"Your brand"** (Promotional content)
  - Check **"Branded content"** (Paid partnership)
- Show that **"Only me"** becomes disabled in the privacy dropdown
- Show the **"Branded content visibility cannot be set to private"** notice
- Show the updated consent text mentioning Branded Content Policy
- Uncheck "Branded content" to show the privacy option re-enables

### Scene 8: Point 4 — Content Preview & Confirmation (10s)
- Click **"Publish Now"**
- Show the **confirmation step** appears with:
  - Account name
  - Title
  - Selected privacy level
  - Selected interaction settings
  - Commercial content status
  - Note: "Content may take a few minutes to process on TikTok"
- This proves the user reviews all settings before publishing

### Scene 9: Point 4 — Publish & Status Tracking (10s)
- Click **"Confirm Publish"**
- Show the **status tracker** appear: "Processing on TikTok..."
- Status updates to show the post is being processed
- Final status shows success or expected sandbox restriction message
- This demonstrates `video.publish` scope and post status polling

### Scene 10: Save as Draft — video.upload (10s)
- Open another video
- Click **"Save as Draft"**
- Show loading → success: "Sent to TikTok inbox as draft!"
- This demonstrates `video.upload` scope

### Scene 11: Landing Page — ToS & Privacy (5s)
- Navigate to `https://tabiji.ai/media/`
- Show **Terms of Service** and **Privacy Policy** links

### End

## Key Points for TikTok Reviewer

1. **Point 1 — Creator Info**: Creator's nickname is displayed before posting; max duration is checked
2. **Point 2 — Metadata**: Privacy dropdown has NO default; user must select. Interaction checkboxes are all unchecked by default, disabled options shown as greyed out
3. **Point 3 — Commercial Content**: Music Usage Confirmation displayed. Commercial content toggle reveals brand/branded checkboxes. Branded content disables private privacy. Consent text updates dynamically
4. **Point 4 — User Control**: Content preview with full settings summary shown before publish. User must explicitly confirm. Status tracker polls for post progress
5. **Point 5 — Security**: `client_secret` kept server-side, never exposed to frontend
6. **All 3 scopes demonstrated**: `user.info.basic`, `video.publish`, `video.upload`
7. **No watermarks or logos** added to content
8. **Users can edit** all preset text, tags, and settings
9. **Domain matches**: All actions happen on tabiji.ai
10. **Sandbox environment**: Using sandbox test user as required
