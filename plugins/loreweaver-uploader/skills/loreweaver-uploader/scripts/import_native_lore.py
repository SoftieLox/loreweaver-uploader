#!/usr/bin/env python3
"""Convert a verified LoreWeaver JSON lore export into the portable world package."""

import argparse
import json
from pathlib import Path
from loreweaver_common import empty_world, unique_slug, write_json


NATIVE_TYPES = {"character", "location", "faction", "item", "event", "misc"}
TYPE_MAP = {"event": "event_history"}


def convert(entries, title, premise):
    if not isinstance(entries, list):
        raise ValueError("LoreWeaver lore export must be a top-level array")
    world = empty_world()
    world["title"] = title
    world["premise"] = premise
    world["source"] = {
        "format": "loreweaver-lore-export",
        "native_contract": "2026-07-06",
        "entry_count": len(entries),
    }
    used = set()
    required = {
        "title", "type", "description", "tags", "importance",
        "pinned", "activeForPrompt", "image",
    }
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValueError(f"entry {index} must be an object")
        missing = required - entry.keys()
        if missing:
            raise ValueError(f"entry {index} missing fields: {', '.join(sorted(missing))}")
        native_type = entry["type"]
        if native_type not in NATIVE_TYPES:
            raise ValueError(f"entry {index} has unsupported type {native_type!r}")
        card_title = str(entry["title"]).strip()
        world["lore_cards"].append({
            "id": unique_slug(card_title or f"entry-{index + 1}", used),
            "type": TYPE_MAP.get(native_type, native_type),
            "title": card_title,
            "content": entry["description"],
            "keywords": list(entry["tags"]),
            "tags": list(entry["tags"]),
            "importance": entry["importance"],
            "pinned": entry["pinned"],
            "prompt_active": entry["activeForPrompt"],
            "private": False,
            "image": entry["image"],
            "extensions": {"native_type": native_type},
        })
    return world


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--title", required=True)
    parser.add_argument("--premise", default="Lore imported from a LoreWeaver JSON lore export.")
    args = parser.parse_args()
    entries = json.loads(Path(args.input).read_text(encoding="utf-8"))
    write_json(args.output, convert(entries, args.title, args.premise))
    print(f"{args.output}\nImported {len(entries)} native lore card(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
