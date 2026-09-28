# Quality

## Code and delivery law
First pass is last pass. No placeholders. Born to work. If it ships, it runs.

## Quality bar — 9+
Every artifact targets **9 or higher** before it is claimed done:

1. **Works** — live path succeeds
2. **Complete** — no placeholders, stubs, or theater
3. **Clear** — purpose and next action obvious
4. **Modern** — current stable best practice for the stack
5. **Innovative where it pays** — cutting-edge when it improves reliability, speed, UX, or maintainability without breaking the outcome
6. **Verified** — health, build, typecheck, or equivalent live check passed
7. **Owned** — proprietary posture; secrets never in git
8. **Discoverable** — status and residual gaps visible for the next pass

A 9+ outcome works at the level we expect. Innovation is desired; broken novelty is not.

## Continuous discovery
While working any repo, skill, or deploy, automatically discover upgrades — outdated deps, vulnerable packages, framework behind patched lines, stale types, missing CI, degraded health, weak UI vs standard, skill/doc drift.

- Safe upgrades: apply in-pass under finish-the-job authority
- Large breaking upgrades: minimal safe step now + residual logged in STATUS
- Prefer doing the upgrade over only listing it
- Prefer automation when the same upgrade will recur

Skills: `quality-continuous-upgrade`, `finish-the-job`, `operator-preferences`

## Definition of Done (any artifact)
- Meets the 9+ bar above
- Answers the eight README questions or equivalent clarity
- Uncertainty is visible where it exists
- Public/private boundary respected
- Cross-links to Grove and relevant services present where appropriate
- STATUS.md and mermicorn.repo.yaml updated
- No secrets, no invented authority claims
- No empty theater
- Live verification performed when a live surface exists

## Rights
Proprietary by default. Collaboration by discussion only.
