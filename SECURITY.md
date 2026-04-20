# Security policy

## Never commit secrets

**Do not commit API keys, tokens, passwords, or other secrets to this repo.**
This is a public repository. Anything you push — even in a deleted file or a
rewritten commit — stays in git history and is indexed by secret scanners.

### What counts as a secret
- API keys / tokens (SerpAPI, SEMrush, OpenAI, Anthropic, Cloudflare, etc.)
- Service account credentials (Google, AWS, Azure)
- OAuth refresh tokens (Instagram, TikTok, YouTube)
- Cloudflare API tokens (not account IDs)
- Gemini / OpenAI / Anthropic API keys
- Unsplash access keys (both "demo" and "production" tiers)
- Any password, private key, or session token

### What is *not* a secret
- Public identifiers: Cloudflare account ID, Google Maps JS embed key
  (restricted by HTTP referrer to `tabiji.ai`), GA measurement IDs
- Dashboard URLs, documentation links

## How to handle secrets instead

**All production code reads secrets from environment variables or the macOS
keychain.** The pattern:

```python
import os, subprocess, sys

def _load_key(env_name, keychain_service):
    value = os.environ.get(env_name)
    if value:
        return value
    try:
        return subprocess.check_output(
            ["security", "find-generic-password", "-s", keychain_service, "-w"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        raise SystemExit(
            f"ERROR: {env_name} not set and '{keychain_service}' not in macOS keychain."
        )

SERPAPI_KEY = _load_key("SERPAPI_KEY", "serpapi-key")
```

**Never** write:
```python
# WRONG — hardcoded fallback leaks the secret into git
API_KEY = os.environ.get("SERPAPI_KEY", "actual-key-here")
```

## Keychain setup

Add keys to the macOS keychain once per machine:

```bash
security add-generic-password -s serpapi-key    -a tabiji -w "YOUR_KEY"
security add-generic-password -s semrush-api-key -a tabiji -w "YOUR_KEY"
security add-generic-password -s gemini-key      -a tabiji -w "YOUR_KEY"
security add-generic-password -s unsplash-access-key -a tabiji -w "YOUR_KEY"
security add-generic-password -s cloudflare-pages-token -a tabiji -w "YOUR_KEY"
security add-generic-password -s cloudflare-api-token   -a tabiji -w "YOUR_KEY"
```

Update a key (rotation):

```bash
security add-generic-password -s serpapi-key -a tabiji -w "NEW_KEY" -U
```

## If you accidentally commit a secret

1. **Rotate the key immediately** — the compromised value must be revoked at
   the provider (SerpAPI dashboard, SEMrush account, Google Cloud Console,
   etc.). Removing the commit does NOT undo the exposure — scanners and
   forks will have captured it.
2. **Notify the team** so anyone using the old key locally updates their
   keychain.
3. **Remove the secret from HEAD** so it can't be re-leaked by a future fork.
   (Git history rewrite with `git filter-repo` or BFG is optional and
   destructive — only worth it for compliance, since rotation is the real
   fix.)

## Known environment / keychain names used in this repo

| Purpose | Env var | Keychain service |
|---------|---------|------------------|
| SerpAPI | `SERPAPI_KEY` | `serpapi-key` |
| SEMrush | `SEMRUSH_API_KEY` | `semrush-api-key` |
| Google Gemini | `GEMINI_KEY` | `gemini-key` |
| Unsplash | `UNSPLASH_ACCESS_KEY` | `unsplash-access-key` |
| Cloudflare Pages | `CLOUDFLARE_PAGES_TOKEN` | `cloudflare-pages-token` |
| Cloudflare API | `CLOUDFLARE_API_TOKEN` | `cloudflare-api-token` |
| Instagram Graph | — | `instagram-access-token` |
| TikTok | — | `tiktok-refresh-token` |
| YouTube Data API | — | `youtube-refresh-token` |

## Scanning

GitHub secret scanning and GitGuardian are enabled on this repo. Before
pushing, sanity-check with:

```bash
git grep -nE "['\"][a-zA-Z0-9_-]{32,}['\"]" -- '*.py' '*.js' '*.sh'
```
and eyeball the results for anything that looks like a real token.
