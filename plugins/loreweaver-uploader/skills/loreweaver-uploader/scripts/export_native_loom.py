#!/usr/bin/env python3
"""Export portable Loom threads in verified LoreWeaver Loom JSON format."""

import argparse
import copy
import json
import uuid
from pathlib import Path
from loreweaver_common import load_json, normalize_world


def source_id(thread):
    existing = thread.get("source_id")
    if existing:
        return str(existing)
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"loreweaver-uploader:{thread.get('id', thread.get('name', 'thread'))}"))


def convert_thread(thread, index):
    return {
        "sourceId": source_id(thread),
        "name": str(thread.get("name") or thread.get("id") or f"Thread {index + 1}"),
        "description": str(thread.get("description", "")),
        "enabled": bool(thread.get("enabled", True)),
        "conditions": copy.deepcopy(thread.get("conditions", [])),
        "conditionLogic": thread.get("condition_logic", "AND"),
        "actions": copy.deepcopy(thread.get("actions", [])),
        "priority": thread.get("priority", 50),
        "sortOrder": thread.get("sort_order", index),
        "tags": copy.deepcopy(thread.get("tags", [])),
        "color": thread.get("color", "#8B5CF6"),
        "fireOnce": thread.get("repeat") == "once",
        "isHidden": not bool(thread.get("visible", True)),
        "maxFires": thread.get("max_fires"),
        "cooldownActions": copy.deepcopy(thread.get("cooldown_actions")),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    world = normalize_world(load_json(args.input))
    threads = [
        convert_thread(thread, index)
        for index, thread in enumerate(world["loom"]["threads"])
        if isinstance(thread, dict)
    ]
    payload = {"version": "1.0", "threads": threads}
    Path(args.output).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{args.output}\nExported {len(threads)} native Loom thread(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
