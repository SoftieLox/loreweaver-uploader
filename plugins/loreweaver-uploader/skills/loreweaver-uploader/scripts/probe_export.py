#!/usr/bin/env python3
"""Emit a content-minimized structural fingerprint of a JSON export."""

import json
import sys
from pathlib import Path


def shape(value, depth=0):
    if depth > 6:
        return {"type": type(value).__name__, "truncated": True}
    if isinstance(value, dict):
        return {
            "type": "object",
            "keys": {str(key): shape(item, depth + 1) for key, item in sorted(value.items())},
        }
    if isinstance(value, list):
        samples = value[:2]
        return {
            "type": "array",
            "count": len(value),
            "samples": [shape(item, depth + 1) for item in samples],
        }
    if isinstance(value, str):
        return {"type": "string", "length": len(value)}
    if value is None:
        return {"type": "null"}
    return {"type": type(value).__name__}


def main():
    if len(sys.argv) != 2:
        print("usage: probe_export.py <export.json>")
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(shape(data), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
