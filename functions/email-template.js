/**
 * Generates an HTML email body for delivering a customer itinerary link.
 * @param {Object} opts
 * @param {string} opts.customerName - Customer's first name
 * @param {string} opts.destination - e.g. "Barcelona, Spain"
 * @param {string} opts.url - Full itinerary URL
 * @param {string} [opts.duration] - e.g. "5 days"
 * @returns {string} HTML email body
 */
function generateEmailHTML({ customerName, destination, url, duration }) {
  const name = customerName || 'there';
  return `<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#F5F0E8;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#F5F0E8;padding:40px 20px;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="background:#FEFCF9;border-radius:16px;overflow:hidden;max-width:600px;">

<!-- Header -->
<tr><td style="background:#2D3A5C;padding:32px 40px;text-align:center;">
  <span style="font-size:28px;font-weight:700;color:#F5F0E8;letter-spacing:-0.02em;">tabiji<span style="color:#C4704B;">.ai</span></span>
</td></tr>

<!-- Body -->
<tr><td style="padding:40px;">
  <h1 style="font-size:24px;font-weight:700;color:#2D3A5C;margin:0 0 16px;line-height:1.3;">
    Your ${destination || ''} itinerary is ready! 🎉
  </h1>
  <p style="font-size:16px;color:#6B5D4F;line-height:1.6;margin:0 0 24px;">
    Hey ${name},
  </p>
  <p style="font-size:16px;color:#6B5D4F;line-height:1.6;margin:0 0 24px;">
    Your personalized${duration ? ' ' + duration : ''} ${destination || ''} itinerary is live and waiting for you. It's packed with specific restaurant picks, hidden gems, timing tips, and interactive maps for each day.
  </p>

  <!-- CTA Button -->
  <table width="100%" cellpadding="0" cellspacing="0" style="margin:8px 0 32px;">
  <tr><td align="center">
    <a href="${url}" style="display:inline-block;background:#C4704B;color:#ffffff;padding:16px 40px;border-radius:10px;text-decoration:none;font-size:18px;font-weight:600;">
      View Your Itinerary →
    </a>
  </td></tr>
  </table>

  <p style="font-size:14px;color:#8B7355;line-height:1.6;margin:0 0 8px;">
    <strong>Your link:</strong> <a href="${url}" style="color:#C4704B;">${url}</a>
  </p>
  <p style="font-size:14px;color:#8B7355;line-height:1.6;margin:0 0 24px;">
    Bookmark it, share it, screenshot it — it's yours forever.
  </p>

  <hr style="border:none;border-top:1px solid #E8DFD0;margin:24px 0;">

  <p style="font-size:14px;color:#8B7355;line-height:1.6;margin:0 0 8px;">
    <strong>Need changes?</strong> Just reply to this email. You get 2 free revisions — we'll update restaurants, swap neighborhoods, adjust the pace, whatever you need.
  </p>
  <p style="font-size:14px;color:#8B7355;line-height:1.6;margin:0;">
    Have an amazing trip! 🌍
  </p>
</td></tr>

<!-- Footer -->
<tr><td style="padding:24px 40px;background:#F5F0E8;text-align:center;border-top:1px solid #E8DFD0;">
  <p style="font-size:13px;color:#8B7355;margin:0;">
    © ${new Date().getFullYear()} tabiji.ai · 旅路 — Every journey begins with a single step.
  </p>
</td></tr>

</table>
</td></tr>
</table>
</body>
</html>`;
}

module.exports = generateEmailHTML;
