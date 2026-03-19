import { applyFilters, buildResult, handleOptions, json, loadCatalog, readInput, scoreSearch, normalizeList } from './_lib.js';

async function handle(context) {
  const input = await readInput(context);
  const catalog = await loadCatalog(context);
  const limit = Math.min(Number(input.limit || 20), 50);
  const query = input.query || input.q || '';
  const entityTypes = normalizeList(input.entity_types || input.entityType);
  const tags = normalizeList(input.tags || input.good_for || input.goodFor);

  let items = applyFilters(catalog.items, input);

  const scored = items
    .map((item) => {
      const { score, matchedOn } = scoreSearch(item, query, {
        city: input.location || input.city,
        entityTypes,
        tags,
      });
      return { item, score, matchedOn };
    })
    .filter(({ score }) => score > 0 || !query)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);

  return json({
    query,
    count: scored.length,
    totalCatalogItems: catalog.items.length,
    results: scored.map(({ item, score, matchedOn }) => buildResult(item, {
      scores: { search: Number((score / 100).toFixed(3)) },
      matchedOn,
    })),
  });
}

export const onRequestGet = handle;
export const onRequestPost = handle;
export const onRequestOptions = handleOptions;
