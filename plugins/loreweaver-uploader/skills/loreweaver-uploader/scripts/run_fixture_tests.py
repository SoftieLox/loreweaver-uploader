#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from loreweaver_common import diff_worlds, load_json, validate_world


ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"


def run(*args):
    return subprocess.run([sys.executable, *map(str, args)], text=True, capture_output=True)


def main():
    failures = []
    for name in ("valid-minimal.json", "valid-loom-world.json", "valid-character.json"):
        errors, _, _ = validate_world(load_json(FIXTURES / name))
        if errors:
            failures.append(f"{name} should be valid: {errors}")
    errors, _, _ = validate_world(load_json(FIXTURES / "invalid-missing-reference.json"))
    if not errors:
        failures.append("invalid fixture was accepted")

    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)
        conversions = [
            ("convert_fictionlab.py", "fictionlab-sample.json"),
            ("convert_character_card.py", "character-card-v2.json"),
            ("convert_lorebook.py", "generic-lorebook.json"),
        ]
        for script, fixture in conversions:
            output = temp / f"{script}.json"
            result = run(ROOT / script, FIXTURES / fixture, output)
            if result.returncode != 0:
                failures.append(f"{script} failed: {result.stderr or result.stdout}")
                continue
            converted_errors, _, _ = validate_world(load_json(output))
            if converted_errors:
                failures.append(f"{script} produced invalid package: {converted_errors}")

        native_world = temp / "native-world.json"
        native_import = run(
            ROOT / "import_native_lore.py",
            FIXTURES / "native-lore-export.json",
            native_world,
            "--title", "Native Fixture",
        )
        if native_import.returncode != 0:
            failures.append(f"import_native_lore failed: {native_import.stdout}")
        else:
            native_errors, _, _ = validate_world(load_json(native_world))
            if native_errors:
                failures.append(f"native import produced invalid package: {native_errors}")
            roundtrip = temp / "native-roundtrip.json"
            native_export = run(ROOT / "export_native_lore.py", native_world, roundtrip)
            if native_export.returncode != 0:
                failures.append(f"export_native_lore failed: {native_export.stdout}")
            elif json.loads(roundtrip.read_text(encoding="utf-8")) != json.loads(
                (FIXTURES / "native-lore-export.json").read_text(encoding="utf-8")
            ):
                failures.append("native lore round-trip changed the verified fixture")

        loom_world = temp / "native-loom-world.json"
        loom_import = run(
            ROOT / "import_native_loom.py",
            FIXTURES / "native-loom-export.json",
            loom_world,
            "--title", "Native Loom Fixture",
        )
        if loom_import.returncode != 0:
            failures.append(f"import_native_loom failed: {loom_import.stdout}")
        else:
            loom_errors, _, _ = validate_world(load_json(loom_world))
            if loom_errors:
                failures.append(f"native Loom import produced invalid package: {loom_errors}")
            loom_roundtrip = temp / "native-loom-roundtrip.json"
            loom_export = run(ROOT / "export_native_loom.py", loom_world, loom_roundtrip)
            if loom_export.returncode != 0:
                failures.append(f"export_native_loom failed: {loom_export.stdout}")
            elif json.loads(loom_roundtrip.read_text(encoding="utf-8")) != json.loads(
                (FIXTURES / "native-loom-export.json").read_text(encoding="utf-8")
            ):
                failures.append("native Loom round-trip changed the verified fixture")

        verify = run(ROOT / "verify_import.py", FIXTURES / "valid-loom-world.json", FIXTURES / "observed-import.json")
        if verify.returncode != 0:
            failures.append(f"verify_import failed: {verify.stdout}")
        analysis = run(ROOT / "analyze_lore.py", FIXTURES / "valid-loom-world.json")
        if analysis.returncode != 0:
            failures.append(f"analyze_lore failed: {analysis.stdout}")
        for script in ("estimate_context.py", "build_playtest_plan.py"):
            utility = run(ROOT / script, FIXTURES / "valid-loom-world.json")
            if utility.returncode != 0:
                failures.append(f"{script} failed: {utility.stdout}")
        public_copy = temp / "public-copy.json"
        prepared = run(ROOT / "prepare_public_copy.py", FIXTURES / "valid-loom-world.json", public_copy)
        if prepared.returncode != 0 or not public_copy.exists():
            failures.append(f"prepare_public_copy failed: {prepared.stdout}")

    original = load_json(FIXTURES / "valid-minimal.json")
    changed = json.loads(json.dumps(original))
    changed["title"] = "Changed title"
    changed["lore_cards"][0]["importance"] = 5
    diff = diff_worlds(original, changed)
    if diff["summary"]["field_changes"] != 1 or diff["summary"]["modified"] != 1:
        failures.append(f"diff summary is wrong: {diff['summary']}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("All LoreWeaver fixture tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
