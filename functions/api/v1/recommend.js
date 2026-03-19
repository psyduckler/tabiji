import { applyFilters, buildResult, handleOptions, json, loadCatalog, rankRecommendations, readInput } from './_lib.js';

async function handle(context) {
  const input = await readInput(context);
  const catalog = await loadCatalog(context);
  const limit = Math.min(Number(input.limit || 10), 25);
  let pool = applyFilters(catalog.items, {
    ...input,
    ...(input.constraints || {}),
  });

  const intent = String(input.intent || '').toLowerCase();
  if (intent.includes('dinner')) {
    pool = pool.filter((item) => item.entityType !== 'place' || /restaurant|bar|izakaya|tapas|steak|ramen|pizza|wine|cocktail|food|nightlife/i.test(`${item.category} ${(item.tags || []).join(' ')}`));
  }
  if (intent.includes('coffee') || intent.includes('work')) {
    pool = pool.filter((item) => item.entityType !== 'place' || /cafe|coffee|wifi|remote_work/i.test(`${item.category} ${(item.tags || []).join(' ')}`));
  }

  const ranked = rankRecommendations(pool, input).slice(0, limit);

  return json({
    intent: input.intent || null,
    count: ranked.length,
    results: ranked.map(({ item, score, why, tradeoffs }) => buildResult(item, {
      score: Number((score / 100).toFixed(3)),
      whyRecommended: why,
      tradeoffs,
    })),
  });
}

export const onRequestGet = handle;
export const onRequestPost = handle;
export const onRequestOptions = handleOptions;
