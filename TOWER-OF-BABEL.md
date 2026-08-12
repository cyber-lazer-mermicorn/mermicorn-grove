# Tower of Babel — Mermicorn Constellation Language Charter

> **Purpose:** Define exactly which languages are allowed on which floors of the stack, why they are there, and how the constellation enforces that in practice.
>
> **Scope:** All repositories listed in MERMACORN-UNIFIED-MASTER-PLAN.md. Grove is the source of truth.

---

## 1. Floors of the Tower

The constellation is intentionally multilingual, but each language is constrained to a floor and a job.

### 1.1 Infrastructure Floor

**Languages:** Bash, YAML

**Responsibilities:**
- Project bootstrapping and scaffolding
- CI/CD orchestration
- Build pipelines (including Rust→WASM)

**Where this lives:**
- `mermicorn-mega-boot` — one-command scaffolds, scripts, templates
- All repos: `.github/workflows/*.yml` (CI), any `build.sh` or `deploy.sh` scripts

**Rules:**
- No application or domain logic in CI or shell scripts.
- Bash exists to glue tools together, not to implement product features.


### 1.2 AI Core Floor

**Languages:** Rust → WASM, Python

**Responsibilities:**
- Token counting, context compression, and budget enforcement
- ML/AI pipelines (text, vision, commerce models)
- Shared AI services used by multiple verticals

**Where this lives:**
- `mermicorn-token-saver` (lane: `ai-core`)
  - Rust core (`rust/src/lib.rs`) compiled to WASM for token counting, budget enforcement, structural compression
  - TypeScript bridge (`wasm/token_saver.ts`) that wraps the WASM module and provides async, lazy-loaded APIs
  - Python core (`core.py`, `compressor.py`) for offline exact counts and pipeline orchestration
- `mermicorn-graphic-ai` (lane: `ai-core`)
  - Python pipelines for image generation, upscaling, and asset management
- `mermicorn-commerce-ai` (lane: `ai-core`)
  - Python pipelines for product scoring, pricing support, and channel packaging

**Rules:**
- Rust is used when performance is critical *and* the code must run at the edge (WASM) across environments.
- Python is used for offline and backend pipelines where rich ML/DS ecosystems are required.
- If an AI core feature can reasonably be shared by multiple repos, it belongs here, not in a vertical.


### 1.3 Application Floor

**Language:** TypeScript

**Responsibilities:**
- UI and edge APIs
- App routing and client/server orchestration
- Consuming AI core services via HTTP, RPC, or WASM bridges

**Where this lives:**
- `vercel-showcase` (and future Next.js / Vercel apps)
- Any frontend or edge route that consumes `mermicorn-token-saver` via the TypeScript bridge
- Future vertical UIs (travel comparison, ravewear gallery, auction dashboards, etc.)

**Rules:**
- TypeScript owns application-level logic, not heavy token counting or ML.
- Edge routes and clients **call** the Rust/Python core; they do not re-implement it.
- All cross-service calls use explicit contracts (JSON over HTTP, JSON over WASM, or typed RPC).


### 1.4 Governance & Metadata Floor

**Languages:** YAML, JSON, Markdown, Python (tooling)

**Responsibilities:**
- Canonical repo metadata (`mermicorn.repo.yaml`)
- Architecture and strategy docs
- Schema definitions and validators

**Where this lives:**
- `mermicorn-grove` (lane: `identity-governance`)
  - `MERMACORN-UNIFIED-MASTER-PLAN.md` — constellation map
  - `ARCHITECTURE.md` — federation principles + shared services
  - `mermicorn.repo.yaml` — Grove’s own metadata
  - `schemas/mermicorn.repo.schema.json` — JSON Schema for all `mermicorn.repo.yaml`
  - `tools/validate_constellation.py` — Python validator that uses GitHub API + JSON Schema
  - `.github/workflows/validate-constellation.yml` — nightly + on-push validation
- `cyber-lazer-mermicorn` (profile repo; lane: `identity-governance`)
  - `mermicorn.repo.yaml` — profile metadata

**Rules:**
- YAML is for human-friendly repo metadata; JSON Schema is the machine-enforced contract.
- Grove is the only repo allowed to define constellation-wide schemas and validation logic.
- Any schema change in Grove must be followed by aligning all affected `mermicorn.repo.yaml` files.

---

## 2. Lanes and Languages

Each repository declares a **lane** in `mermicorn.repo.yaml`. The lane determines which languages are expected and which responsibilities it may own.

### 2.1 Lanes (from schema)

From `schemas/mermicorn.repo.schema.json`:

- `identity-governance` — Grove, profile, and any repo that defines who Cherry is and how the constellation is wired.
- `ai-core` — shared AI services (boot, memory, token-saver, graphics, commerce).
- `commerce` — revenue-generating verticals (ravewear, travel, numismatic auctions, auto, etc.).
- `gaming` — gaming and community projects (Rift Lab, Chance Game Lab).
- `career` — operator apprenticeship and career development.
- `private-ops` — private operational repos (vaults, private-ops, internal logs).

Each lane has an allowed language set:

- **identity-governance**: YAML, JSON, Markdown, Python (tooling only).
- **ai-core**: Rust→WASM, Python, TypeScript (bridges and clients), Bash/YAML for build + CI.
- **commerce**: TypeScript (apps), Python (analysis), SQL (DB logic), Bash/YAML for CI; AI core features are consumed rather than re-implemented.
- **gaming**: TypeScript (UIs, bots), Python (data analysis), SQL as needed.
- **career**: Markdown (curriculum), TypeScript/Python as needed for exercises or automation.
- **private-ops**: Python, YAML, SQL, and internal tooling — no public-facing UIs without explicit design.

---

## 3. Boundary Contracts

The Tower keeps languages from bleeding into each other by enforcing explicit contracts at every boundary.

### 3.1 WASM Boundary (Rust ↔ TypeScript)

- Rust exposes `count_tokens`, `enforce_budget`, and `compress` via `wasm-bindgen`.
- TypeScript bridge (`wasm/token_saver.ts`) lazy-loads the WASM and provides async functions:
  - `countTokens(text)`
  - `enforceTokenBudget(text, maxTokens)`
  - `compressContext(text)`
  - `prepareContext(text, maxTokens)`
- All data across this boundary is JSON-serializable structures.

**Rule:** No Rust code is imported directly from application code; all access goes through the bridge.


### 3.2 Service Boundary (Python ↔ TypeScript)

- Python services (graphic-ai, commerce-ai, future travel/auction engines) expose HTTP APIs with clearly typed JSON bodies.
- TypeScript clients or server actions call these APIs and treat them as black boxes.

**Rule:** Business logic that can live in AI core or backend services must not be duplicated in the front-end.


### 3.3 Metadata Boundary (YAML ↔ JSON Schema ↔ Python)

- Each repo contains `mermicorn.repo.yaml` at the root, following the schema.
- Grove’s `mermicorn.repo.schema.json` defines required fields and enums.
- `tools/validate_constellation.py` fetches every `mermicorn.repo.yaml` via the GitHub API and validates it nightly.

**Rule:** If the schema and a yaml disagree, the schema wins and yaml files must be brought back into compliance.

---

## 4. Rules of the Tower

1. **No language freelancing.**
   - Introducing a new language or moving responsibilities across languages requires updating this charter and Grove’s architecture docs first.

2. **No duplicated responsibility.**
   - Token counting, context compression, and budget enforcement belong to `mermicorn-token-saver` (Rust/WASM + Python mirror).
   - Visual pipelines belong to `mermicorn-graphic-ai`.
   - Commerce packaging belongs to `mermicorn-commerce-ai`.
   - Metadata schemas and constellation validation belong to `mermicorn-grove`.

3. **Contracts at every boundary.**
   - WASM boundaries use JSON-serializable structures only.
   - Service boundaries use documented APIs.
   - Metadata boundaries use YAML + JSON Schema.

4. **Simple for Cherry.**
   - Cherry does not need to think about which language to use; the lane and floor decide.
   - Grove, schemas, and CI keep the system coherent so Cherry can focus on design, deals, and artifacts.

---

## 5. How to Propose a Change

1. Update `TOWER-OF-BABEL.md` in `mermicorn-grove` with the proposed change.
2. Update `ARCHITECTURE.md` and, if needed, `MERMACORN-UNIFIED-MASTER-PLAN.md` to reflect the new responsibilities.
3. Update `schemas/mermicorn.repo.schema.json` if the change affects lanes, statuses, or required fields.
4. Update affected `mermicorn.repo.yaml` files across the constellation.
5. Run `python tools/validate_constellation.py` locally until it passes.
6. Open a PR explaining the change and link to the artifacts that motivated it.

This keeps the Tower of Babel coherent, on purpose, and always in service of real, publishable work.