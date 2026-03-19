import { applyFilters, buildResult, handleOptions, json, loadCatalog, readInput } from './_lib.js';

async function handle(context) {
  const input = await readInput(context);
  const catalog = await loadCatalog(context);
  const limit = Math.min(Number(input.limit || 30), 100);
  const filtered = applyFilters(catalog.items, input).slice(0, limit);

  return json({
    constraints: input,
    count: filtered.length,
    results: filtered.map((item) => buildResult(item)),
  });
}

export const onRequestGet = handle;
export const onRequestPost = handle;
export const onRequestOptions = handleOptions;
