# Architecture — mermicorn-grove

## Role

mermicorn-grove is the **integration state** of the entire constellation.
It does not own any vertical — it observes and enforces that every repo
is correctly structured so the constellation stays coherent.

## Language Map

| Layer | Language | Why |
|-------|----------|-----|
| Constellation validator | **Python** | GitHub API calls, YAML parsing, JSON Schema validation — the correct tool for scripted CI work against live APIs |
| Schema definition | **JSON Schema** | Language-neutral contract; every editor (VS Code, IntelliJ) validates yaml against it automatically |
| Repo metadata | **YAML** | `mermicorn.repo.yaml` — human-readable, editor-friendly, parseable by every language in the constellation |
| Registry docs | **Markdown** | Human-readable source of truth |
| CI orchestration | **YAML** (GitHub Actions) | Runs the Python validator on push + nightly |

## Boundary Contracts

```
GitHub Actions (validate-constellation.yml)
    │  runs on push to main + nightly cron
    ↓
tools/validate_constellation.py  (Python)
    │  fetches mermicorn.repo.yaml from each of the 15 repos via GitHub API
    │  validates against schemas/mermicorn.repo.schema.json (JSON Schema Draft 7)
    │  prints human-readable report + writes validation-report.json
    │  exits 0 (all valid) or 1 (any invalid/missing) — fails CI on drift
    ↓
schemas/mermicorn.repo.schema.json  (JSON Schema)
    │  defines required fields: schema_version, id, display_name, owner,
    │  lane, visibility, status, purpose.problem, purpose.audience
    │  used by the Python validator AND by VS Code YAML extension for inline hints
```

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

## How to Run the Validator Locally

```bash
# Install deps
pip install -r requirements.txt

# Validate all 15 repos
export GITHUB_TOKEN=ghp_...
python tools/validate_constellation.py

# Validate one repo
python tools/validate_constellation.py --repo mermicorn-token-saver

# Write a JSON report
python tools/validate_constellation.py --output report.json
```

Exit 0 → all repos valid. Exit 1 → schema drift detected. Exit 2 → config/auth error.
