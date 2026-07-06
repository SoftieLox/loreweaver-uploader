#!/usr/bin/env python3
"""Create a verified LoreWeaver-compatible JSON lore export from a portable package."""

import argparse
import json
from pathlib import Path
from loreweaver_common import load_json, normalize_world


TYPE_MAP = {
    "character": "character",
    "location": "location",
    "faction": "faction",
    "item": "item",
    "event": "event",
    "event_history": "event",
    "misc": "misc",
    "concept": "misc",
    "lore": "misc",
    "world_rule": "misc",
}


def convert(world):
    entries = []
    warnings = []
    for index, card in enumerate(normalize_world(world)["lore_cards"]):
        if not isinstance(card, dict):
            continue
        card_type = card.get("type", "lore")
        native_type = TYPE_MAP.get(card_type)
        if native_type is None:
            native_type = "misc"
            warnings.append(f"card {card.get('id', index)!r}: mapped unknown type {card_type!r} to 'misc'")
        tags = card.get("tags")
        if not tags:
            tags = card.get("keywords", [])
        entries.append({
            "title": str(card.get("title", "")),
            "type": native_type,
            "description": str(card.get("content", "")),
            "tags": [str(tag) for tag in tags],
            "importance": card.get("importance", 3),
            "pinned": bool(card.get("pinned", False)),
            "activeForPrompt": bool(card.get("prompt_active", True)),
            "image": card.get("image"),
        })
    return entries, warnings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    entries, warnings = convert(load_json(args.input))
    Path(args.output).write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{args.output}\nExported {len(entries)} native lore card(s).")
    for warning in warnings:
        print(f"WARNING: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
