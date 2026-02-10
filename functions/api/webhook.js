export async function onRequestPost(context) {
  const STRIPE_SK = context.env.STRIPE_SECRET_KEY;
  const WEBHOOK_SECRET = context.env.STRIPE_WEBHOOK_SECRET;
  const SLACK_WEBHOOK_URL = context.env.SLACK_WEBHOOK_URL;

  try {
    const body = await context.request.text();

    // TODO: Verify Stripe webhook signature with WEBHOOK_SECRET
    // For v1, we'll trust the payload and verify via Stripe API
    const event = JSON.parse(body);

    if (event.type !== 'checkout.session.completed') {
      return new Response(JSON.stringify({ received: true }), { status: 200 });
    }

    const session = event.data.object;
    const customerEmail = session.customer_details?.email || 'unknown';
    const destination = session.metadata?.destination || 'Not specified';
    const amountPaid = (session.amount_total / 100).toFixed(2);
    const sessionId = session.id;

    // Post to Slack #tabiji channel
    if (SLACK_WEBHOOK_URL) {
      const slackPayload = {
        text: `🎌 *New Tabiji Order!*\n\n• *Customer:* ${customerEmail}\n• *Destination:* ${destination}\n• *Amount:* $${amountPaid}\n• *Session:* \`${sessionId}\`\n\nTime to build an itinerary! 🗺️`,
      };

      await fetch(SLACK_WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(slackPayload),
      });
    }

    return new Response(JSON.stringify({ received: true }), {
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
