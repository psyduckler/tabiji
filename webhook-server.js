const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8787;
const OPENCLAW_PORT = 18789;
const HOOKS_TOKEN = process.env.OPENCLAW_HOOKS_TOKEN || '';
const ORDERS_DIR = path.join(__dirname, 'orders');
const PENDING_FILE = path.join(ORDERS_DIR, 'pending.json');

// Helper: POST to OpenClaw hooks API
function postToOpenClaw(endpoint, payload, label) {
  const data = JSON.stringify(payload);
  const req = http.request({
    hostname: '127.0.0.1',
    port: OPENCLAW_PORT,
    path: `/hooks/${endpoint}`,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(data),
      'Authorization': `Bearer ${HOOKS_TOKEN}`,
    },
  }, (res) => {
    let body = '';
    res.on('data', c => body += c);
    res.on('end', () => console.log(`${label} [${res.statusCode}]:`, body));
  });
  req.on('error', (err) => console.error(`${label} failed:`, err.message));
  req.write(data);
  req.end();
}

// Notify #tabiji Slack channel about new order
function notifySlack(order) {
  const lines = [
    `🎌 *New Itinerary Request!*`,
    `• *Destination:* ${order.destination}`,
    `• *Dates:* ${order.start_date} → ${order.end_date}`,
    `• *Group:* ${order.group_size}`,
    `• *Email:* ${order.email}`,
  ];
  if (order.travel_style) lines.push(`• *Style:* ${order.travel_style}`);
  if (order.dining) lines.push(`• *Dining:* ${order.dining}`);
  if (order.budget) lines.push(`• *Budget:* ${order.budget}`);
  if (order.requests) lines.push(`• *Requests:* ${order.requests}`);
  lines.push(`• *Order ID:* \`${order.id}\``);

  // Use wake event to notify main session, which will handle Slack + fulfillment
  // The wake text includes all order details so the agent can act on it
}

// Wake OpenClaw to fulfill the order
function triggerFulfillment(order) {
  const wakeText = [
    `New tabiji.ai itinerary order received!`,
    `Customer: ${order.email}`,
    `Destination: ${order.destination}`,
    `Dates: ${order.start_date} to ${order.end_date}`,
    `Group size: ${order.group_size}`,
    order.travel_style ? `Travel style: ${order.travel_style}` : '',
    order.dining ? `Dining: ${order.dining}` : '',
    order.budget ? `Budget: ${order.budget}` : '',
    order.requests ? `Special requests: ${order.requests}` : '',
    `Order ID: ${order.id}`,
    ``,
    `Fulfill this order: spawn a sub-agent to research, generate the itinerary, publish to /i/ (slug format: /i/xxxx-xxxx, both words 4 letters), email the customer, and update pending.json.`,
  ].filter(Boolean).join('\n');

  postToOpenClaw('wake', { text: wakeText, mode: 'now' }, 'Wake event');
}

// Save order to pending.json
function saveOrder(order) {
  let pending = [];
  try { pending = JSON.parse(fs.readFileSync(PENDING_FILE, 'utf8')); } catch {}
  pending.push(order);
  fs.writeFileSync(PENDING_FILE, JSON.stringify(pending, null, 2));
}

// Ensure orders directory exists
if (!fs.existsSync(ORDERS_DIR)) fs.mkdirSync(ORDERS_DIR, { recursive: true });

const server = http.createServer((req, res) => {
  // Stripe webhook
  if (req.method === 'POST' && req.url === '/webhook') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const event = JSON.parse(body);
        if (event.type !== 'checkout.session.completed') {
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ received: true }));
          return;
        }

        const session = event.data.object;
        const order = {
          id: session.id,
          email: session.customer_details?.email || session.metadata?.email || 'unknown',
          destination: session.metadata?.destination || 'Not specified',
          start_date: session.metadata?.start_date || '',
          end_date: session.metadata?.end_date || '',
          group_size: session.metadata?.group_size || '',
          travel_style: session.metadata?.travel_style || '',
          dining: session.metadata?.dining || '',
          budget: session.metadata?.budget || '',
          requests: session.metadata?.requests || '',
          amount: (session.amount_total / 100).toFixed(2),
          timestamp: new Date().toISOString(),
          status: 'pending'
        };

        saveOrder(order);
        console.log(`🎌 NEW ORDER: ${order.destination} for ${order.email} ($${order.amount})`);
        triggerFulfillment(order);

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ received: true, order_id: session.id }));
      } catch (err) {
        console.error('Webhook error:', err.message);
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
      }
    });

  // Direct form submission (free)
  } else if (req.method === 'POST' && req.url === '/order') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      res.setHeader('Access-Control-Allow-Origin', 'https://tabiji.ai');
      res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
      res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
      try {
        const data = JSON.parse(body);
        const order = {
          id: 'order_' + Date.now() + '_' + Math.random().toString(36).slice(2, 8),
          email: data.email || 'unknown',
          destination: data.destination || 'Not specified',
          start_date: data.start_date || '',
          end_date: data.end_date || '',
          group_size: data.group_size || '',
          travel_style: data.travel_style || '',
          dining: data.dining || '',
          budget: data.budget || '',
          requests: data.requests || '',
          amount: '0.00',
          timestamp: new Date().toISOString(),
          status: 'pending'
        };

        saveOrder(order);
        console.log(`🎌 NEW ORDER: ${order.destination} for ${order.email} (free)`);
        triggerFulfillment(order);

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true, order_id: order.id }));
      } catch (err) {
        console.error('Order error:', err.message);
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, error: err.message }));
      }
    });

  // CORS preflight
  } else if (req.method === 'OPTIONS' && req.url === '/order') {
    res.setHeader('Access-Control-Allow-Origin', 'https://tabiji.ai');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.writeHead(204);
    res.end();

  // Health check
  } else if (req.method === 'GET' && req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', timestamp: new Date().toISOString() }));

  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`🎌 Tabiji webhook server running on http://127.0.0.1:${PORT}`);
});
