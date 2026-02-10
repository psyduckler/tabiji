const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8787;
const ORDERS_DIR = path.join(__dirname, 'orders');
const PENDING_FILE = path.join(ORDERS_DIR, 'pending.json');

// Ensure orders directory exists
if (!fs.existsSync(ORDERS_DIR)) fs.mkdirSync(ORDERS_DIR, { recursive: true });

const server = http.createServer((req, res) => {
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

        // Append to pending orders file
        let pending = [];
        try { pending = JSON.parse(fs.readFileSync(PENDING_FILE, 'utf8')); } catch {}
        pending.push(order);
        fs.writeFileSync(PENDING_FILE, JSON.stringify(pending, null, 2));

        console.log(`🎌 NEW ORDER: ${order.destination} for ${order.email} ($${order.amount})`);

        // Wake OpenClaw to fulfill the order
        const wakeText = `New tabiji.ai order! Customer: ${order.email}, Destination: ${order.destination}, Dates: ${order.start_date} to ${order.end_date}, Group: ${order.group_size}, Style: ${order.travel_style}, Dining: ${order.dining}, Budget: ${order.budget}, Requests: ${order.requests}. Check /Users/psy/.openclaw/workspace/tabiji/orders/pending.json and fulfill this order.`;
        try {
          const { execSync } = require('child_process');
          execSync(`curl -s -X POST http://127.0.0.1:4152/api/cron/wake -H "Content-Type: application/json" -d '${JSON.stringify({ text: wakeText, mode: "now" })}'`, { timeout: 5000 });
          console.log('OpenClaw wake event sent');
        } catch (wakeErr) {
          console.error('Wake event failed:', wakeErr.message);
        }

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ received: true, order_id: session.id }));
      } catch (err) {
        console.error('Webhook error:', err.message);
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
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
