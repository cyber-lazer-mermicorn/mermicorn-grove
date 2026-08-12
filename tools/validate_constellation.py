#!/usr/bin/env python3
"""
validate_constellation.py
=========================
Reads every mermicorn.repo.yaml in the constellation via the GitHub API,
validates each against schemas/mermicorn.repo.schema.json, and reports
any schema drift.

This turns mermicorn-grove from a documentation repo into a live machine
that enforces federation across all 15 repositories.

Usage:
    # Validate all repos (requires GITHUB_TOKEN env var)
    python tools/validate_constellation.py

    # Validate a single repo
    python tools/validate_constellation.py --repo mermicorn-token-saver

    # Write a JSON report
    python tools/validate_constellation.py --output report.json

Exit codes:
    0  All repos valid
    1  One or more repos have schema violations or missing yaml
    2  Configuration/auth error
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import requests
import yaml
from jsonschema import Draft7Validator, ValidationError

# ── Constellation registry ──────────────────────────────────────────────────────────
# The canonical list of all 15 constellation repos.
# Source of truth: MERMACORN-UNIFIED-MASTER-PLAN.md

ORG = "cyber-lazer-mermicorn"

CONSTELLATION_REPOS = [
    # Identity & Command
    "cyber-lazer-mermicorn",
    "mermicorn-grove",
    # Shared AI Operating Core
    "mermicorn-mega-boot",
    "mermicorn-memory",
    "mermicorn-token-saver",
    "mermicorn-graphic-ai",
    "mermicorn-commerce-ai",
    "mermicorn-private-ops",
    # Commerce Ventures
    "cherry-ravewear-studio",
    "cherry-travel-deal-lab",
    "cherry-numismatic-auction-lab",
    "cherry-auto-matchmaker",
    # Gaming & Community
    "cherry-rift-lab",
    "cherry-chance-game-lab",
    # Career Development
    "cherry-operator-apprenticeship",
]

YAML_FILE = "mermicorn.repo.yaml"
SCHEMA_FILE = Path(__file__).parent.parent / "schemas" / "mermicorn.repo.schema.json"


# ── Result types ───────────────────────────────────────────────────────────────────

@dataclass
class RepoResult:
    repo: str
    status: str  # "valid" | "invalid" | "missing" | "error"
    errors: list[str] = field(default_factory=list)
    data: dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.status == "valid"


# ── GitHub fetcher ──────────────────────────────────────────────────────────────────

def fetch_yaml(repo: str, token: str) -> tuple[dict | None, str | None]:
    """
    Fetch mermicorn.repo.yaml from the default branch of *repo*.
    Returns (parsed_dict, None) on success or (None, error_message).
    """
    url = f"https://api.github.com/repos/{ORG}/{repo}/contents/{YAML_FILE}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.raw+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as exc:
        return None, f"network error: {exc}"

    if resp.status_code == 404:
        return None, "MISSING"
    if resp.status_code == 403:
        return None, f"forbidden (check token scopes): {resp.status_code}"
    if resp.status_code != 200:
        return None, f"HTTP {resp.status_code}"

    try:
        parsed = yaml.safe_load(resp.text)
        if not isinstance(parsed, dict):
            return None, "YAML parsed to non-dict"
        return parsed, None
    except yaml.YAMLError as exc:
        return None, f"YAML parse error: {exc}"


# ── Validator ──────────────────────────────────────────────────────────────────────

def validate_repo(repo: str, token: str, validator: Draft7Validator) -> RepoResult:
    parsed, error = fetch_yaml(repo, token)

    if error == "MISSING":
        return RepoResult(repo=repo, status="missing", errors=[f"{YAML_FILE} not found"])
    if error:
        return RepoResult(repo=repo, status="error", errors=[error])

    schema_errors = [
        f"{'.'.join(str(p) for p in e.absolute_path) or '(root)'}: {e.message}"
        for e in sorted(validator.iter_errors(parsed), key=lambda e: e.absolute_path)
    ]

    if schema_errors:
        return RepoResult(repo=repo, status="invalid", errors=schema_errors, data=parsed)

    return RepoResult(repo=repo, status="valid", data=parsed)


# ── Reporter ──────────────────────────────────────────────────────────────────────

STATUS_ICON = {
    "valid": "\u2705",
    "invalid": "\u274c",
    "missing": "\u26a0\ufe0f ",
    "error": "\U0001f4a5",
}


def print_report(results: list[RepoResult]) -> None:
    total = len(results)
    valid = sum(1 for r in results if r.status == "valid")
    invalid = sum(1 for r in results if r.status == "invalid")
    missing = sum(1 for r in results if r.status == "missing")
    errors = sum(1 for r in results if r.status == "error")

    print()
    print("\u2500" * 60)
    print("  Mermicorn Constellation Validator")
    print("\u2500" * 60)

    for r in results:
        icon = STATUS_ICON[r.status]
        print(f"  {icon}  {r.repo:<40} {r.status.upper()}")
        for err in r.errors:
            print(f"       └─ {err}")

    print("\u2500" * 60)
    print(f"  {total} repos checked | {valid} valid | {invalid} invalid | {missing} missing | {errors} errors")
    print("\u2500" * 60)
    print()


# ── Main ─────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Mermicorn constellation repos")
    parser.add_argument("--repo", help="Validate a single repo (default: all)")
    parser.add_argument("--output", help="Write JSON report to this file")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("ERROR: GITHUB_TOKEN environment variable not set.", file=sys.stderr)
        print("  export GITHUB_TOKEN=ghp_...", file=sys.stderr)
        return 2

    if not SCHEMA_FILE.exists():
        print(f"ERROR: Schema not found at {SCHEMA_FILE}", file=sys.stderr)
        return 2

    schema = json.loads(SCHEMA_FILE.read_text())
    validator = Draft7Validator(schema)

    repos = [args.repo] if args.repo else CONSTELLATION_REPOS

    print(f"Validating {len(repos)} repo(s) against {SCHEMA_FILE.name}…")
    results = [validate_repo(r, token, validator) for r in repos]

    print_report(results)

    if args.output:
        report = [
            {"repo": r.repo, "status": r.status, "errors": r.errors, "id": r.data.get("id", "")}
            for r in results
        ]
        Path(args.output).write_text(json.dumps(report, indent=2))
        print(f"Report written to {args.output}")

    all_ok = all(r.ok for r in results)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
