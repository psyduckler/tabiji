import { onRequestPost as __api_checkout_js_onRequestPost } from "/Users/psy/.openclaw/workspace/tabiji/functions/api/checkout.js"
import { onRequestPost as __api_webhook_js_onRequestPost } from "/Users/psy/.openclaw/workspace/tabiji/functions/api/webhook.js"

export const routes = [
    {
      routePath: "/api/checkout",
      mountPath: "/api",
      method: "POST",
      middlewares: [],
      modules: [__api_checkout_js_onRequestPost],
    },
  {
      routePath: "/api/webhook",
      mountPath: "/api",
      method: "POST",
      middlewares: [],
      modules: [__api_webhook_js_onRequestPost],
    },
  ]