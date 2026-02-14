/**
 * Generates a plain-text email body for delivering a customer itinerary link.
 * @param {Object} opts
 * @param {string} opts.customerName - Customer's first name
 * @param {string} opts.destination - e.g. "Barcelona, Spain"
 * @param {string} opts.url - Full itinerary URL
 * @param {string} [opts.duration] - e.g. "5 days"
 * @param {string[]} [opts.highlights] - List of itinerary highlights
 * @returns {string} Plain text email body
 */
function generateEmailText({ customerName, destination, url, duration, highlights }) {
  const name = customerName || 'there';
  const dur = duration ? ` ${duration}` : '';
  
  let body = `Hey ${name},

Your personalized${dur} ${destination || ''} itinerary is ready!

View it here: ${url}

`;

  if (highlights && highlights.length) {
    body += `What's inside:\n`;
    highlights.forEach(h => { body += `• ${h}\n`; });
    body += `\n`;
  }

  body += `Bookmark it, share it, or pull it up on your phone during your trip — it's yours forever.

Need changes? Just reply to this email. You get 2 free revisions — we'll update restaurants, swap neighborhoods, adjust the pace, whatever you need.

Have an amazing trip! 🌍

— tabiji.ai
旅路 — Every journey begins with a single step.
`;

  return body;
}

module.exports = generateEmailText;
