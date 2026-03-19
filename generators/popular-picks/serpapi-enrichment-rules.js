#!/usr/bin/env node

const ALLOWED_DIETARY_TAGS = [
  'vegetarian-friendly',
  'vegetarian-options',
  'vegan-options',
  'gluten-free-options',
  'gluten-free-fries',
  'halal',
];

const ALLOWED_PAYMENT_HINTS = [
  'cash-only',
  'cards-accepted',
  'credit-cards-accepted',
  'digital-payments',
  'cash',
  'pin',
  'credit-card',
];

const ALLOWED_TOURISTY_LEVELS = [
  'mostly-local',
  'mixed',
  'mixed-leaning-touristy',
  'touristy',
  'tourist-magnet',
];

const ALLOWED_MEAL_TYPES = [
  'breakfast',
  'brunch',
  'lunch',
  'dinner',
  'late-night',
  'drinks',
  'snack',
  'snack / lunch',
  'lunch / dinner',
  'dinner / late-night',
  'dinner / late-night / drinks',
  'sunset drinks',
  'sunset drinks / dinner / late-night',
  'sunset drinks / late-night',
];

const ALLOWED_CONFIDENCE = ['low', 'medium', 'medium-high', 'high'];

const ALLOWED_SOURCE_TYPES = [
  'google-serp-kg',
  'official-site',
  'booking-page',
  'menu-page',
  'faq-page',
  'brand-page',
  'reservation-snippet',
  'dress-code-page',
  'dress-code-snippet',
  'tripadvisor-snippet',
  'happycow-snippet',
  'instagram-snippet',
  'facebook-snippet',
  'travel-blog-snippet',
  'promo-snippet',
  'promo-page',
  'delivery-snippet',
  'thefork-snippet',
  'opentable-snippet',
  'quandoo-snippet',
  'kimpton-page',
  'skywalk-page',
  'attraction-page',
  'venue-guide-snippet',
  'yelp-snippet',
  'google-places',
  'legacy-html',
  'reddit',
];

const SOURCE_PRIORITY = {
  reservationNeeded: ['booking-page', 'official-site', 'faq-page', 'reservation-snippet', 'google-serp-kg', 'tripadvisor-snippet', 'yelp-snippet'],
  bestTimeToGo: ['google-serp-kg', 'official-site', 'promo-snippet', 'instagram-snippet', 'tripadvisor-snippet', 'reddit'],
  waitExpectation: ['google-serp-kg', 'reservation-snippet', 'tripadvisor-snippet', 'yelp-snippet', 'reddit'],
  mealType: ['google-serp-kg', 'menu-page', 'official-site', 'tripadvisor-snippet'],
  dietaryTags: ['official-site', 'menu-page', 'happycow-snippet', 'tripadvisor-snippet', 'google-serp-kg'],
  paymentHints: ['official-site', 'faq-page', 'tripadvisor-snippet', 'yelp-snippet'],
  touristyLevel: ['google-serp-kg', 'tripadvisor-snippet', 'reddit', 'travel-blog-snippet'],
  knownForTags: ['official-site', 'menu-page', 'google-serp-kg', 'tripadvisor-snippet', 'reddit'],
};

module.exports = {
  ALLOWED_DIETARY_TAGS,
  ALLOWED_PAYMENT_HINTS,
  ALLOWED_TOURISTY_LEVELS,
  ALLOWED_MEAL_TYPES,
  ALLOWED_CONFIDENCE,
  ALLOWED_SOURCE_TYPES,
  SOURCE_PRIORITY,
};
