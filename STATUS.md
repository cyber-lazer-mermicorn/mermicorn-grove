# Status

**State:** OPERATING / constellation upgrade in progress  
**Last updated:** 2026-08-14

## Truth

- **10 Vercel projects** under team cyber-lazerwrmicorn
- **9 READY**, **1 ERROR** (`cherry-rental-engine` — single failed deploy; Git may not be pushing new builds)
- Public product domains on `*.lazermermicorn.com` are live for portfolio, ravewear, commerce, deals, autos, coins, rift, games, learn
- Stripe account connected (Hi-Class Home services); rental Stripe code is on GitHub `main` but not yet on a successful Vercel deploy

## Canonical upgrade board

See [docs/VERCEL-CONSTELLATION-UPGRADE.md](./docs/VERCEL-CONSTELLATION-UPGRADE.md)

## Immediate blockers (human)

1. Link + redeploy `cherry-rental-engine` from latest `main`
2. Paste Supabase service role + Stripe keys into Vercel env
3. Register Stripe webhook endpoint

## Not claimed

- Do not claim all ten projects were deeply rewritten in one pass
- Do not claim rental is live until deploy state is READY
