export async function onRequestPost(context) {
  const STRIPE_SK = context.env.STRIPE_SECRET_KEY;
  const SITE_URL = context.env.SITE_URL || 'https://tabiji.ai';
  const PRICE_ID = context.env.STRIPE_PRICE_ID || 'price_1Sz99KGsCD9VM6IJvKQJq2C9';

  try {
    const body = await context.request.json().catch(() => ({}));
    const destination = body.destination || '';

    const params = new URLSearchParams();
    params.append('mode', 'payment');
    params.append('success_url', `${SITE_URL}/success?session_id={CHECKOUT_SESSION_ID}`);
    params.append('cancel_url', `${SITE_URL}/#pricing`);
    params.append('line_items[0][price]', PRICE_ID);
    params.append('line_items[0][quantity]', '1');
    params.append('payment_method_types[0]', 'card');
    params.append('metadata[destination]', destination);

    // Let Stripe collect email during checkout
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
