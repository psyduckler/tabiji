const fs = require('fs');
const path = require('path');
const fulfillOrder = require('../functions/fulfill-order');

// Load the data parts
const base = JSON.parse(fs.readFileSync(path.join(__dirname, 'tokyo-veg-base.json'), 'utf8'));
const day1 = JSON.parse(fs.readFileSync(path.join(__dirname, 'tokyo-veg-day1.json'), 'utf8'));
const day2 = JSON.parse(fs.readFileSync(path.join(__dirname, 'tokyo-veg-day2.json'), 'utf8'));
const day3 = JSON.parse(fs.readFileSync(path.join(__dirname, 'tokyo-veg-day3.json'), 'utf8'));
const day4 = JSON.parse(fs.readFileSync(path.join(__dirname, 'tokyo-veg-day4.json'), 'utf8'));
const day5 = JSON.parse(fs.readFileSync(path.join(__dirname, 'tokyo-veg-day5.json'), 'utf8'));
const extras = JSON.parse(fs.readFileSync(path.join(__dirname, 'tokyo-veg-extras.json'), 'utf8'));

// Combine
const itineraryData = {
  ...base.data,
  days: [day1, day2, day3, day4, day5],
  ...extras
};

const order = base.order;

console.log('Order:', order.id);
console.log('Destination:', itineraryData.destination);
console.log('Days:', itineraryData.days.length);
console.log('Budget rows:', itineraryData.budgetTable.length);
console.log('Practical sections:', itineraryData.practicalInfo.length);
console.log('');
console.log('Starting fulfillment...');

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('\n✅ FULFILLMENT COMPLETE');
  console.log('Slug:', result.slug);
  console.log('URL:', result.url);
  console.log('Email sent:', result.emailSent);
} catch (err) {
  console.error('\n❌ FULFILLMENT FAILED:', err.message);
  process.exit(1);
}
