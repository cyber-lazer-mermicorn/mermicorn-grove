# Connectors — quality & function board

**Updated:** 2026-08-22  
**Canonical YAML:** `constellation-map/registry/connectors.yml`

## Operator MCP (live probes this session)

| Connector | Status | Function | Quality action |
|-----------|--------|----------|----------------|
| **GitHub** | Ready | Repos, push, Actions | Keep CI using `npm install` until lockfiles exist |
| **Vercel** | Ready | 10 projects / domains | Force rental redeploy from latest `main` |
| **Stripe** | Ready (livemode) | Hi-Class Home services | Paste keys + webhook on rental Vercel |
| **Calendly** | Ready | `cyber-lazer-mermicorn` · 30min + Meet · HST | Embed on hire + host dashboard |
| **Google Calendar** | Ready | Primary + Family | Optional busy-time → rental blocks |
| **Gmail / Outlook** | Ready | Human inbox ops | Product mail stays on Resend |
| **Linear** | Ready | Issue tracking | Track P0 connector env gaps |
| **Automations** | Empty | Scheduled agent tasks | Add health digest automation |
| **Voice** | Ready | TTS | Optional demos |

## Product runtime (cherry-rental-engine)

| Connector | Endpoint / surface | Status |
|-----------|-------------------|--------|
| Supabase | typed clients + service role | Schema ready; env on Vercel required |
| Stripe | `/api/stripe/checkout-session`, `/api/stripe/webhook` | Code ready |
| iCal | `/api/ical/import`, `/api/ical/[listingId]` | Parser hardened (RFC unfold + datetime) |
| Calendly | `GET /api/calendly` | Public URLs |
| Health matrix | `GET /api/health` | Reports all connector readiness |
| Resend | message queue → send | Needs `RESEND_API_KEY` |

## Quality bar

1. **Secrets never in git** — only Vercel / local `.env`
2. **Health is honest** — `partial` / `missing` preferred over fake `ok`
3. **Public vs private** — Calendly URLs public; Stripe secrets server-only
4. **One spine for money** — Stripe Checkout + signed webhooks
5. **One spine for host time** — Calendly for humans; iCal for channel blocks

## Immediate human checklist

1. Vercel rental env: Supabase service role + Stripe secret + webhook secret  
2. Stripe Dashboard webhook → production `/api/stripe/webhook`  
3. Optional: `RESEND_API_KEY`, `CRON_SECRET`  
4. Embed Calendly 30min on portfolio Hire + rental host UI  
5. After deploy: `GET /api/health` should show connector matrix  
