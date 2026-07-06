#!/usr/bin/env python3
"""Dependency-free release checks for the public marketplace repository."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    if not MARKETPLACE.is_file():
        fail("missing .agents/plugins/marketplace.json", errors)
        marketplace = {}
    else:
        marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))

    if marketplace.get("name") != "softielox":
        fail("marketplace name must be 'softielox'", errors)
    entries = marketplace.get("plugins", [])
    if not isinstance(entries, list) or len(entries) != 1:
        fail("marketplace must contain exactly one plugin entry", errors)
        entries = []

    for entry in entries:
        required_entry = {"name", "source", "policy", "category"}
        missing = required_entry - entry.keys()
        if missing:
            fail(f"marketplace entry missing: {sorted(missing)}", errors)
            continue
        source_path = entry.get("source", {}).get("path")
        if source_path != "./plugins/loreweaver-uploader":
            fail("marketplace source path is incorrect", errors)

    plugin = ROOT / "plugins" / "loreweaver-uploader"
    manifest_path = plugin / ".codex-plugin" / "plugin.json"
    if not manifest_path.is_file():
        fail("missing plugin manifest", errors)
        manifest = {}
    else:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    if manifest.get("name") != plugin.name:
        fail("plugin folder and manifest names differ", errors)
    if not SEMVER.fullmatch(str(manifest.get("version", ""))):
        fail("plugin version is not valid semantic versioning", errors)
    if manifest.get("author", {}).get("name") != "SoftieLox":
        fail("creator name must be SoftieLox", errors)
    if manifest.get("license") != "MIT":
        fail("manifest license must be MIT", errors)

    interface = manifest.get("interface", {})
    for field in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        if not interface.get(field):
            fail(f"missing interface.{field}", errors)
    for field in ("composerIcon", "logo"):
        value = interface.get(field)
        if not value or not (plugin / value.removeprefix("./")).is_file():
            fail(f"missing interface asset: {field}", errors)
    for screenshot in interface.get("screenshots", []):
        path = plugin / str(screenshot).removeprefix("./")
        if path.suffix.lower() != ".png" or not path.is_file():
            fail(f"invalid screenshot asset: {screenshot}", errors)

    forbidden = []
    for path in plugin.rglob("*"):
        if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
            forbidden.append(str(path.relative_to(ROOT)))
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".py"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            if "[TODO:" in text:
                fail(f"placeholder remains in {path.relative_to(ROOT)}", errors)
    if forbidden:
        fail(f"generated Python files committed: {forbidden}", errors)

    skill = plugin / "skills" / "loreweaver-uploader" / "SKILL.md"
    if not skill.is_file():
        fail("missing LoreWeaver skill", errors)
    else:
        text = skill.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "name: loreweaver-uploader" not in text:
            fail("invalid skill frontmatter", errors)

    fixture_runner = plugin / "skills" / "loreweaver-uploader" / "scripts" / "run_fixture_tests.py"
    if not errors:
        completed = subprocess.run(
            [sys.executable, str(fixture_runner)],
            cwd=fixture_runner.parent,
            text=True,
            capture_output=True,
        )
        print(completed.stdout, end="")
        if completed.returncode:
            print(completed.stderr, end="", file=sys.stderr)
            fail("fixture tests failed", errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Marketplace release validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
