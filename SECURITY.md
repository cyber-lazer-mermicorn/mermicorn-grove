# Security

## Rules
- Never commit passwords, API keys, payment credentials, or customer payment data.
- Use GitHub Secrets or an external vault for sensitive values.
- `mermicorn-memory` and `mermicorn-private-ops` remain private and still contain no secrets.
- Public repositories may hold sanitized portfolio work, templates, and schemas only.
- Report potential exposure immediately and rotate credentials.

## Scanning
Dependency alerts and secret scanning should be enabled on all repositories where available.
