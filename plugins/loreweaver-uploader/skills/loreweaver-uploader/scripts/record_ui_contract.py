#!/usr/bin/env python3
import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from loreweaver_common import load_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("observed")
    parser.add_argument("current")
    parser.add_argument("history")
    args = parser.parse_args()
    data = load_json(args.observed)
    data["recorded_at"] = datetime.now(timezone.utc).isoformat()
    history = Path(args.history)
    history.mkdir(parents=True, exist_ok=True)
    current = Path(args.current)
    if current.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        shutil.copy2(current, history / f"ui-contract-{stamp}.json")
    current.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(current)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
