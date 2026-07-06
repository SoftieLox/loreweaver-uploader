#!/usr/bin/env python3
import sys
from loreweaver_common import load_json, validate_world


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_world.py <world.json>")
        return 2
    try:
        data = load_json(sys.argv[1])
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    errors, warnings, info = validate_world(data)

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")
    for message in info:
        print(f"INFO: {message}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
