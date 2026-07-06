#!/usr/bin/env python3
import json
import sys
from loreweaver_common import load_json


def main():
    if len(sys.argv) != 3:
        print("usage: check_ui_contract.py <expected-contract.json> <observed-contract.json>")
        return 2
    expected = load_json(sys.argv[1])
    observed = load_json(sys.argv[2])
    errors, warnings = [], []
    for surface, expected_surface in expected.get("surfaces", {}).items():
        actual = observed.get("surfaces", {}).get(surface)
        if actual is None:
            errors.append(f"missing surface: {surface}")
            continue
        expected_controls = set(expected_surface.get("required_controls", []))
        actual_controls = set(actual.get("controls", []))
        for missing in sorted(expected_controls - actual_controls):
            errors.append(f"{surface}: missing required control {missing!r}")
        for extra in sorted(actual_controls - expected_controls):
            warnings.append(f"{surface}: unrecognized control {extra!r}")
    print(json.dumps({"errors": errors, "warnings": warnings, "compatible": not errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
