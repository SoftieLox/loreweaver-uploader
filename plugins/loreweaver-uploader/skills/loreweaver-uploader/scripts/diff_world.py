#!/usr/bin/env python3
import json
import sys
from loreweaver_common import diff_worlds, load_json


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: diff_world.py <current.json> <proposed.json>")
        return 2
    diff = diff_worlds(load_json(sys.argv[1]), load_json(sys.argv[2]))
    print(json.dumps(diff, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
