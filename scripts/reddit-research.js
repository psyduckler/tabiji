#!/usr/bin/env node

const USER_AGENT = process.env.REDDIT_USER_AGENT || 'tabiji-reddit-helper/0.1';

function usage() {
  console.error(`Usage:
  reddit-research.js subreddit <subreddit> [--sort hot|new|top|rising] [--limit N] [--time day|week|month|year|all]
  reddit-research.js search <query> [--subreddit NAME] [--sort relevance|hot|top|new|comments] [--time hour|day|week|month|year|all] [--limit N]
  reddit-research.js thread <post-id-or-url> [--comment-limit N] [--depth N]
  reddit-research.js comments <subreddit> [--limit N]

Outputs JSON to stdout.`);
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token.startsWith('--')) {
      const key = token.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith('--')) {
        args[key] = true;
      } else {
        args[key] = next;
        i += 1;
      }
    } else {
      args._.push(token);
    }
  }
  return args;
}

function intValue(value, fallback) {
  const n = Number.parseInt(value, 10);
  return Number.isFinite(n) ? n : fallback;
}

function buildUrl(path, params = {}) {
  const url = new URL(`https://www.reddit.com${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null && value !== '') url.searchParams.set(key, String(value));
  }
  return url;
}

async function fetchJson(url) {
  const response = await fetch(url, {
    headers: {
      'user-agent': USER_AGENT,
      'accept': 'application/json',
    },
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Reddit request failed (${response.status} ${response.statusText}) for ${url}: ${text.slice(0, 300)}`);
  }

  return response.json();
}

function simplifyPost(post) {
  return {
    id: post.id,
    name: post.name,
    subreddit: post.subreddit,
    title: post.title,
    author: post.author,
    score: post.score,
    numComments: post.num_comments,
    createdUtc: post.created_utc,
    permalink: `https://www.reddit.com${post.permalink}`,
    url: post.url,
    selftext: post.selftext || '',
    over18: !!post.over_18,
    spoiler: !!post.spoiler,
    stickied: !!post.stickied,
    isSelf: !!post.is_self,
    linkFlairText: post.link_flair_text || null,
  };
}

function flattenComments(children, acc = [], depth = 0, maxDepth = Infinity) {
  if (!Array.isArray(children) || depth > maxDepth) return acc;
  for (const child of children) {
    if (!child || child.kind !== 't1' || !child.data) continue;
    const c = child.data;
    acc.push({
      id: c.id,
      parentId: c.parent_id,
      author: c.author,
      body: c.body || '',
      score: c.score,
      depth,
      createdUtc: c.created_utc,
      permalink: c.permalink ? `https://www.reddit.com${c.permalink}` : null,
      distinguished: c.distinguished || null,
      stickied: !!c.stickied,
    });
    if (c.replies && typeof c.replies === 'object' && c.replies.data) {
      flattenComments(c.replies.data.children, acc, depth + 1, maxDepth);
    }
  }
  return acc;
}

function normalizePostIdOrUrl(input) {
  if (/^https?:\/\//.test(input)) {
    const match = input.match(/comments\/([a-z0-9]+)\//i);
    if (!match) throw new Error(`Could not extract post id from URL: ${input}`);
    return match[1];
  }
  return input;
}

async function run() {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];

  if (!command) {
    usage();
    process.exit(1);
  }

  if (command === 'subreddit') {
    const subreddit = args._[1];
    if (!subreddit) throw new Error('Missing subreddit');
    const sort = args.sort || 'hot';
    const limit = Math.min(intValue(args.limit, 10), 100);
    const time = args.time;
    const url = buildUrl(`/r/${subreddit}/${sort}.json`, { limit, t: time, raw_json: 1 });
    const json = await fetchJson(url);
    const items = (json.data?.children || []).map((item) => simplifyPost(item.data));
    console.log(JSON.stringify({ command, subreddit, sort, time: time || null, count: items.length, items }, null, 2));
    return;
  }

  if (command === 'search') {
    const query = args._.slice(1).join(' ').trim();
    if (!query) throw new Error('Missing search query');
    const limit = Math.min(intValue(args.limit, 10), 100);
    const sort = args.sort || 'relevance';
    const time = args.time || 'all';
    const subreddit = args.subreddit || null;
    const path = subreddit ? `/r/${subreddit}/search.json` : '/search.json';
    const url = buildUrl(path, {
      q: query,
      restrict_sr: subreddit ? 'on' : undefined,
      sort,
      t: time,
      limit,
      type: 'link',
      raw_json: 1,
    });
    const json = await fetchJson(url);
    const items = (json.data?.children || []).map((item) => simplifyPost(item.data));
    console.log(JSON.stringify({ command, query, subreddit, sort, time, count: items.length, items }, null, 2));
    return;
  }

  if (command === 'thread') {
    const input = args._[1];
    if (!input) throw new Error('Missing post id or URL');
    const postId = normalizePostIdOrUrl(input);
    const commentLimit = Math.min(intValue(args['comment-limit'], 20), 500);
    const depth = intValue(args.depth, 3);
    const url = buildUrl(`/comments/${postId}.json`, {
      limit: commentLimit,
      depth,
      raw_json: 1,
      sort: 'top',
    });
    const json = await fetchJson(url);
    const post = json?.[0]?.data?.children?.[0]?.data;
    const commentChildren = json?.[1]?.data?.children || [];
    const comments = flattenComments(commentChildren, [], 0, depth);
    console.log(JSON.stringify({
      command,
      post: post ? simplifyPost(post) : null,
      requestedCommentLimit: commentLimit,
      requestedDepth: depth,
      commentCount: comments.length,
      comments,
    }, null, 2));
    return;
  }

  if (command === 'comments') {
    const subreddit = args._[1];
    if (!subreddit) throw new Error('Missing subreddit');
    const limit = Math.min(intValue(args.limit, 10), 100);
    const url = buildUrl(`/r/${subreddit}/comments.json`, { limit, raw_json: 1 });
    const json = await fetchJson(url);
    const items = (json.data?.children || []).filter((item) => item.kind === 't1').map((item) => ({
      id: item.data.id,
      author: item.data.author,
      body: item.data.body || '',
      score: item.data.score,
      createdUtc: item.data.created_utc,
      permalink: item.data.permalink ? `https://www.reddit.com${item.data.permalink}` : null,
      linkTitle: item.data.link_title || null,
      linkPermalink: item.data.link_permalink ? `https://www.reddit.com${item.data.link_permalink}` : null,
      subreddit: item.data.subreddit,
    }));
    console.log(JSON.stringify({ command, subreddit, count: items.length, items }, null, 2));
    return;
  }

  usage();
  throw new Error(`Unknown command: ${command}`);
}

run().catch((error) => {
  console.error(error.message || String(error));
  process.exit(1);
});
