#!/usr/bin/env python3
import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from loreweaver_common import load_json, slugify


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    snap = sub.add_parser("snapshot")
    snap.add_argument("world")
    snap.add_argument("history")
    listing = sub.add_parser("list")
    listing.add_argument("history")
    restore = sub.add_parser("restore")
    restore.add_argument("snapshot")
    restore.add_argument("output")
    args = parser.parse_args()

    if args.command == "snapshot":
        data = load_json(args.world)
        history = Path(args.history)
        history.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        destination = history / f"{slugify(str(data.get('title', 'world')))}-{stamp}.json"
        destination.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(destination)
    elif args.command == "list":
        for path in sorted(Path(args.history).glob("*.json")):
            print(path)
    else:
        shutil.copy2(args.snapshot, args.output)
        print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
