# Architecture

## Federation Principles

- mermicorn-grove owns integration state and status
- Each vertical is independently useful
- Shared services (boot, memory, token-saver, graphic-ai, commerce-ai) are consumed, not duplicated
- Data policy is explicit per repo (public templates vs private credentials / customer data)

## Shared Services

| Service | Role |
|---------|------|
| mermicorn-mega-boot | Scaffold compliant projects |
| mermicorn-memory | Preferences, evidence, continuity (private) |
| mermicorn-token-saver | Context compression and budgets |
| mermicorn-graphic-ai | Visual system and asset generation |
| mermicorn-commerce-ai | Product → listing → sales package |
