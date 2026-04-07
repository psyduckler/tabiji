const fulfillOrder = require('./functions/fulfill-order');
const data = require('/tmp/molokai-full-data.json');

const order = {
  id: 'order_1773073630484_lczlvy',
  orderId: 'order_1773073630484_lczlvy',
  email: 'kialogy@gmail.com',
  destination: 'Kualapuu, HI, USA',
  startDate: '2026-05-11',
  endDate: '2026-05-17',
  customerName: null
};

try {
  const result = fulfillOrder(order, data);
  console.log('\n✅ FULFILLMENT COMPLETE');
  console.log('Slug:', result.slug);
  console.log('URL:', result.url);
  console.log('Email sent:', result.emailSent);
} catch (err) {
  console.error('\n❌ FULFILLMENT FAILED:', err.message);
  process.exit(1);
}
