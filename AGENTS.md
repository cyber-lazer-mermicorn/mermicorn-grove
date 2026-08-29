# Mermicorn Grove — Agent Doctrine

## What this repo is
Canonical constellation registry for Cyber Lazer Mermicorn / Cherry. The single source of truth for what exists, its status, and integration topology.

## Rules
- This repo is READ authority only for agents — never add business logic here
- Constellation registry in `registry/` — one YAML/JSON per vertical
- Integration map in `integrations/` — describes connections between repos/services
- Status tracked as: `active`, `in-progress`, `planned`, `archived`
- All repos must appear here before they are considered part of the constellation
- No code in this repo — only registry documents, maps, and status files

## Commands
```bash
python -m grove validate    # validate registry schema
python -m grove status      # print constellation status
```

## Do not
- Add application code to this repo
- Register a repo as `active` without a working demo
- Remove repos without archiving them first
