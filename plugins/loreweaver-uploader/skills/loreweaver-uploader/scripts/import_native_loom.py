#!/usr/bin/env python3
"""Import a verified LoreWeaver Loom thread export into a portable world package."""

import argparse
import copy
import json
from pathlib import Path
from loreweaver_common import empty_world, load_json, unique_slug, write_json


THREAD_FIELDS = {
    "sourceId", "name", "description", "enabled", "conditions", "conditionLogic",
    "actions", "priority", "sortOrder", "tags", "color", "fireOnce",
    "isHidden", "maxFires", "cooldownActions",
}


def convert_thread(thread, used, index):
    missing = THREAD_FIELDS - thread.keys()
    if missing:
        raise ValueError(f"thread {index} missing fields: {', '.join(sorted(missing))}")
    name = str(thread["name"]).strip() or f"Thread {index + 1}"
    return {
        "id": unique_slug(name, used),
        "source_id": thread["sourceId"],
        "name": name,
        "description": thread["description"],
        "enabled": thread["enabled"],
        "conditions": copy.deepcopy(thread["conditions"]),
        "condition_logic": thread["conditionLogic"],
        "actions": copy.deepcopy(thread["actions"]),
        "priority": thread["priority"],
        "sort_order": thread["sortOrder"],
        "tags": copy.deepcopy(thread["tags"]),
        "color": thread["color"],
        "repeat": "once" if thread["fireOnce"] else "repeat",
        "visible": not thread["isHidden"],
        "max_fires": thread["maxFires"],
        "cooldown_actions": copy.deepcopy(thread["cooldownActions"]),
    }


def convert(source, base=None, title="Imported Loom Threads"):
    if not isinstance(source, dict) or not isinstance(source.get("threads"), list):
        raise ValueError("LoreWeaver Loom export must be an object containing a threads array")
    if source.get("version") != "1.0":
        raise ValueError(f"unsupported Loom export version {source.get('version')!r}")
    world = copy.deepcopy(base) if base is not None else empty_world()
    if base is None:
        world["title"] = title
        world["premise"] = "Loom Engine threads imported from LoreWeaver."
    used = set()
    world.setdefault("loom", {})["threads"] = [
        convert_thread(thread, used, index)
        for index, thread in enumerate(source["threads"])
    ]
    world["loom"].setdefault("variables", [])
    world["loom"].setdefault("quests", [])
    world["loom"].setdefault("inventory", [])
    world["loom"].setdefault("hud", {})
    world.setdefault("source", {})["loom"] = {
        "format": "loreweaver-loom-export",
        "version": source["version"],
        "native_contract": "2026-07-06",
        "thread_count": len(source["threads"]),
    }
    return world


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--base")
    parser.add_argument("--title", default="Imported Loom Threads")
    args = parser.parse_args()
    source = json.loads(Path(args.input).read_text(encoding="utf-8"))
    base = load_json(args.base) if args.base else None
    world = convert(source, base=base, title=args.title)
    write_json(args.output, world)
    print(f"{args.output}\nImported {len(source['threads'])} native Loom thread(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
