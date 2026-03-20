#!/usr/bin/env python3
"""Build the Tokyo fulfillment script from JSON data."""
import json, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCRIPT_DIR, "fulfill-order_1773933372257_6e4kmc.js")

# Build complete itinerary data as Python dict, then serialize to JS
data = json.load(open(os.path.join(SCRIPT_DIR, "_tokyo_data.json")))

js = f"""const fulfillOrder = require('../functions/fulfill-order');

const order = {{
  id: 'order_1773933372257_6e4kmc',
  email: 'bernard.j.huang@gmail.com',
  destination: 'Tokyo, Japan',
  startDate: '2026-03-20',
  endDate: '2026-03-23',
  groupSize: 1,
}};

const itineraryData = {json.dumps(data, indent=2, ensure_ascii=False)};

try {{
  const result = fulfillOrder(order, itineraryData);
  console.log('\\u2705 Fulfilled:', JSON.stringify(result, null, 2));
}} catch (err) {{
  console.error('\\u274c Error:', err.message);
  process.exit(1);
}}
"""

with open(OUT, 'w') as f:
    f.write(js)

print(f"Written {len(js)} bytes to {OUT}")
