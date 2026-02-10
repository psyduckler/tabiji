export async function onRequestPost(context) {
  const STRIPE_SK = context.env.STRIPE_SECRET_KEY;

  try {
    const body = await context.request.text();
    const event = JSON.parse(body);

    if (event.type !== 'checkout.session.completed') {
      return new Response(JSON.stringify({ received: true }), { status: 200 });
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

    // Store order in KV if available, otherwise just respond
    if (context.env.ORDERS) {
      // Cloudflare KV binding
      const orders = JSON.parse(await context.env.ORDERS.get('pending') || '[]');
      orders.push(order);
      await context.env.ORDERS.put('pending', JSON.stringify(orders));
    }

    return new Response(JSON.stringify({ received: true, order_id: session.id }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
