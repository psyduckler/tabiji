const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8787;
const ORDERS_DIR = path.join(__dirname, 'orders');
const PENDING_FILE = path.join(ORDERS_DIR, 'pending.json');

// Save order to pending.json
function saveOrder(order) {
  let pending = [];
  try { pending = JSON.parse(fs.readFileSync(PENDING_FILE, 'utf8')); } catch {}
  pending.push(order);
  fs.writeFileSync(PENDING_FILE, JSON.stringify(pending, null, 2));
}

// Wake OpenClaw so it picks up the new order
function wakeOpenClaw(order) {
  const token = process.env.OPENCLAW_HOOKS_TOKEN;
  if (!token) { console.log('⚠️ No OPENCLAW_HOOKS_TOKEN, skipping wake'); return; }
  const payload = JSON.stringify({
    text: `New tabiji order: ${order.destination} for ${order.email}. Check orders/pending.json and fulfill it.`
  });
  const opts = {
    hostname: '127.0.0.1',
    port: 18789,
    path: '/hooks/wake',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      'Content-Length': Buffer.byteLength(payload)
    }
  };
  const req = http.request(opts, (res) => {
    let body = '';
    res.on('data', c => body += c);
    res.on('end', () => console.log(`Wake event [${res.statusCode}]: ${body}`));
  });
  req.on('error', (err) => console.error('Wake error:', err.message));
  req.write(payload);
  req.end();
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
        wakeOpenClaw(order);

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

        // Dedup: skip if same email+destination already pending
        let existing = [];
        try { existing = JSON.parse(fs.readFileSync(PENDING_FILE, 'utf8')); } catch {}
        const isDupe = existing.some(o =>
          o.email === order.email &&
          o.destination === order.destination &&
          o.start_date === order.start_date &&
          o.status === 'pending'
        );
        if (isDupe) {
          console.log(`⚠️ DUPLICATE ORDER skipped: ${order.destination} for ${order.email}`);
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ ok: true, duplicate: true }));
          return;
        }

        saveOrder(order);
        console.log(`🎌 NEW ORDER: ${order.destination} for ${order.email} (free)`);
        wakeOpenClaw(order);

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

// Graceful shutdown — close server so port is released before exit
function shutdown(signal) {
  console.log(`🎌 Received ${signal}, shutting down gracefully...`);
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(1), 3000); // force exit after 3s
}
process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));

// Handle port conflict: kill stale process and retry
const { execSync } = require('child_process');
const MAX_RETRIES = 3;
let retries = 0;

function startServer() {
  server.listen(PORT, '127.0.0.1', () => {
    console.log(`🎌 Tabiji webhook server running on http://127.0.0.1:${PORT}`);
  });
}

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE' && retries < MAX_RETRIES) {
    retries++;
    console.log(`⚠️ Port ${PORT} in use (attempt ${retries}/${MAX_RETRIES}). Killing stale process...`);
    try {
      const output = execSync(`/usr/sbin/lsof -ti :${PORT}`).toString().trim();
      const pids = output.split('\n').filter(p => p && Number(p) !== process.pid);
      for (const pid of pids) {
        console.log(`🔪 Killing stale PID ${pid}`);
        try { process.kill(Number(pid), 'SIGTERM'); } catch {}
      }
    } catch {}
    setTimeout(startServer, 2000);
  } else {
    console.error('❌ Fatal server error:', err.message);
    process.exit(1);
  }
});

startServer();
