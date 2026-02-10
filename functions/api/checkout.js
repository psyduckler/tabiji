export async function onRequestPost(context) {
  const STRIPE_SK = context.env.STRIPE_SECRET_KEY;
  const SITE_URL = context.env.SITE_URL || 'https://tabiji.ai';
  const PRICE_ID = context.env.STRIPE_PRICE_ID || 'price_1Sz99KGsCD9VM6IJvKQJq2C9';

  try {
    const body = await context.request.json().catch(() => ({}));

    const destination = body.destination || '';
    const startDate = body.start_date || '';
    const endDate = body.end_date || '';
    const groupSize = body.group_size || '';
    const travelStyle = body.travel_style || '';
    const dining = body.dining || '';
    const budget = body.budget || '';
    const requests = (body.requests || '').slice(0, 500);
    const email = body.email || '';

    const params = new URLSearchParams();
    params.append('mode', 'payment');
    params.append('success_url', `${SITE_URL}/success?session_id={CHECKOUT_SESSION_ID}`);
    params.append('cancel_url', `${SITE_URL}/plan`);
    params.append('line_items[0][price]', PRICE_ID);
    params.append('line_items[0][quantity]', '1');
    params.append('payment_method_types[0]', 'card');

    // Pass trip details as Stripe metadata
    params.append('metadata[destination]', destination);
    params.append('metadata[start_date]', startDate);
    params.append('metadata[end_date]', endDate);
    params.append('metadata[group_size]', groupSize);
    params.append('metadata[travel_style]', travelStyle);
    params.append('metadata[dining]', dining);
    params.append('metadata[budget]', budget);
    params.append('metadata[requests]', requests);
    params.append('metadata[email]', email);

    // Pre-fill customer email if provided
    if (email) {
      params.append('customer_email', email);
    }
    params.append('customer_creation', 'always');

    const res = await fetch('https://api.stripe.com/v1/checkout/sessions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${STRIPE_SK}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: params.toString(),
    });

    const session = await res.json();

    if (session.error) {
      return new Response(JSON.stringify({ error: session.error.message }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    return new Response(JSON.stringify({ url: session.url }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
