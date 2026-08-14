# Vercel Constellation Upgrade Board

**Audit date:** 2026-08-14 HST  
**Team:** `team_zIICQt0OuE84nAXpNARduTbP` (cyber-lazerwrmicorn)

## Live deployment health

| # | Vercel project | Domain | Framework | State | Priority |
|---|----------------|--------|-----------|-------|----------|
| 1 | cherry-rental-engine | cherry-rental-engine-cyber-lazerwrmicorn.vercel.app | nextjs | **ERROR** | P0 |
| 2 | cherry-portfolio | lazermermicorn.com | static | READY | P1 |
| 3 | cherry-ravewear-studio | ravewear.lazermermicorn.com | fastapi | READY | P1 |
| 4 | mermicorn-commerce-ai | commerce.lazermermicorn.com | fastapi | READY | P1 |
| 5 | ai-deal-finder | deals.lazermermicorn.com | fastapi | READY | P2 |
| 6 | cherry-auto-matchmaker | autos.lazermermicorn.com | fastapi | READY | P2 |
| 7 | cherry-numismatic-auction-lab | coins.lazermermicorn.com | fastapi | READY | P2 |
| 8 | cherry-rift-lab | rift.lazermermicorn.com | fastapi | READY | P3 |
| 9 | cherry-chance-game-lab | games.lazermermicorn.com | fastapi | READY | P3 |
| 10 | cherry-operator-apprenticeship | learn.lazermermicorn.com | fastapi | READY | P3 |

**Score:** 9/10 READY · 1/10 ERROR

## P0 — Unblock rental (money path)

`cherry-rental-engine` has **only one deployment ever**, and it is ERROR.  
Git pushes to `main` (Stripe integration, typed foundation) have **not** produced a new production deploy.

### Required human actions
1. Confirm Git is linked: Vercel → Project → Settings → Git → `cyber-lazer-mermicorn/cherry-rental-engine` · branch `main`
2. Redeploy from latest commit (or empty commit to trigger)
3. Env vars (Production + Preview):
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `STRIPE_SECRET_KEY`
   - `STRIPE_WEBHOOK_SECRET`
4. Stripe webhook → `https://<prod-domain>/api/stripe/webhook`

### Code already on main (not yet live)
- Next.js 15.5.23 + typed Supabase
- Stripe Checkout + signed webhook
- iCal import/export, availability, pricing, dashboard, auth
- CI fixed to `npm install` (no lockfile dependency)

## P1 — Flagship product upgrades

### cherry-portfolio (lazermermicorn.com)
- Keep static HTML fast; add explicit vertical deep-links to all READY domains
- Ensure sitemap lists every product domain
- Machine-readable constellation block for recruiters

### cherry-ravewear-studio
- Drop 001 commerce path: listing → checkout handoff via commerce-ai or Stripe
- Asset pipeline when Drop 001 media lands
- Health + version endpoint on FastAPI surface

### mermicorn-commerce-ai
- Shared product record → multichannel package is the commercial spine
- Stripe + Resend env alignment with rental
- Rate-limit + auth on write APIs

## P2 — Vertical depth

| Project | Intelligent upgrade |
|---------|---------------------|
| ai-deal-finder | Real fare sources or honest mock-mode badge; Honolulu-origin presets; shareable deal cards |
| cherry-auto-matchmaker | Intake → comps → packet; connect to commerce package output |
| cherry-numismatic-auction-lab | Provenance flags + comps; listing export to commerce |

## P3 — Lab / education

| Project | Upgrade |
|---------|---------|
| cherry-rift-lab | Build guide quality + responsible play framing |
| cherry-chance-game-lab | Probability education UX; no deceptive patterns |
| cherry-operator-apprenticeship | Module ladder with real artifacts, not placeholders |

## Cross-cutting standards (all projects)

1. **Health** — every deployable app exposes `GET /health` or `/api/health` with `{ status, service, timestamp }`
2. **STATUS.md** — last updated date + live URL + known blockers
3. **Secrets** — never in repo; only Vercel env
4. **CI** — typecheck/lint/test where TypeScript; pytest where Python
5. **Rights** — proprietary default; RIGHTS.md present
6. **Domains** — product.*.lazermermicorn.com is the public face

## What "upgrade pass" means here

Not a simultaneous rewrite of ten codebases.  
Order of operations:

1. **Make production true** — rental green + Stripe keys
2. **Wire money** — portfolio + ravewear + commerce point at working checkout
3. **Deepen one vertical at a time** — deal-finder or auto-matchmaker next
4. **Labs stay honest** — education quality over fake completeness

## Agent execution notes

- Vercel MCP cannot set env vars or force Git reconnect — human required
- GitHub MCP can push code; deploy only happens if Git integration is live
- Prefer first-pass-is-last-pass on any single vertical deep work
