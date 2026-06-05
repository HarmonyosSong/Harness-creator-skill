#!/usr/bin/env python3
"""Validate the minimal Harness framework shape in a target repository."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REQUIRED_DIRS = [
    "harness_Engineering/knowledge",
    "harness_Engineering/agents",
    "harness_Engineering/scripts",
    "harness_Engineering/runtime",
    "harness_Engineering/archive",
]

REQUIRED_FILES = [
    "harness_Engineering/README.md",
    "harness_Engineering/runtime/.gitignore",
    "harness_Engineering/scripts/harness-index.sh",
    "harness_Engineering/scripts/preflight-context.sh",
]


def find_harness_entry(root: Path) -> list[Path]:
    return sorted(path for path in root.glob("*_Harness.md") if path.is_file())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", help="target repository root")
    parser.add_argument(
        "--mode",
        choices=["skeleton", "full", "plugin"],
        default="skeleton",
        help="validation strictness; plugin validates only Codex Plugin distribution shape",
    )
    parser.add_argument(
        "--plugin",
        action="store_true",
        help="also validate Codex Plugin distribution shape with skeleton/full modes",
    )
    args = parser.parse_args()

    root = Path(args.repo).resolve()
    failures: list[str] = []

    if not root.exists() or not root.is_dir():
        print(f"FAIL: repo does not exist: {root}")
        return 2

    validate_harness = args.mode != "plugin"
    validate_plugin = args.plugin or args.mode == "plugin"

    entries: list[Path] = []
    if validate_harness:
        entries = find_harness_entry(root)
        if not entries:
            failures.append("missing *_Harness.md entry file")

        for rel in REQUIRED_DIRS:
            if not (root / rel).is_dir():
                failures.append(f"missing directory: {rel}")

        for rel in REQUIRED_FILES:
            if not (root / rel).is_file():
                failures.append(f"missing file: {rel}")

    if validate_plugin:
        plugin_json = root / ".codex-plugin" / "plugin.json"
        if not plugin_json.is_file():
            failures.append("missing file: .codex-plugin/plugin.json")
        else:
            try:
                manifest = json.loads(plugin_json.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                failures.append(f"invalid JSON: .codex-plugin/plugin.json: {exc}")
            else:
                for key in ["name", "version", "description", "skills"]:
                    if not manifest.get(key):
                        failures.append(f"plugin.json missing required field: {key}")
                skills_dir = manifest.get("skills")
                if isinstance(skills_dir, str):
                    if not (root / skills_dir).is_dir():
                        failures.append(f"plugin.json skills path does not exist: {skills_dir}")
                else:
                    failures.append("plugin.json field must be a string: skills")
                if "[TODO:" in plugin_json.read_text(encoding="utf-8"):
                    failures.append("plugin.json contains TODO placeholder")
        skill_file = root / "skills" / "harness-framework-deployer" / "SKILL.md"
        if not skill_file.is_file():
            failures.append("missing file: skills/harness-framework-deployer/SKILL.md")

    if args.mode == "full":
        full_files = [
            "harness_Engineering/knowledge/module-routing.md",
            "harness_Engineering/agents/orchestrator.md",
            "harness_Engineering/agents/context-explorer-agent.md",
            "harness_Engineering/agents/reviewer-agent.md",
            "harness_Engineering/scripts/postflight-check.sh",
        ]
        for rel in full_files:
            if not (root / rel).is_file():
                failures.append(f"missing full-mode file: {rel}")

    if failures:
        print("FAIL: Harness deployment validation failed")
        for item in failures:
            print(f"- {item}")
        return 1

    if validate_harness:
        print("PASS: Harness deployment shape is valid")
    if validate_plugin:
        print("plugin_distribution: valid")
    if entries:
        print("entry_files:")
        for entry in entries:
            print(f"- {entry.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
