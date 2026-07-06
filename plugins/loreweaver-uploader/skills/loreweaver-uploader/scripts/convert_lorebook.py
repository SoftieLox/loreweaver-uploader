#!/usr/bin/env python3
import argparse
from loreweaver_common import empty_world, load_json, unique_slug, write_json


def convert(source):
    world = empty_world()
    world["title"] = source.get("name") or source.get("title") or "Imported Lorebook"
    world["premise"] = source.get("description") or "A world imported from an external lorebook."
    world["source"] = {"format": "generic-lorebook"}
    entries = source.get("entries", [])
    if isinstance(entries, dict):
        entries = list(entries.values())
    used = set()
    for index, entry in enumerate(entries):
        title = str(entry.get("name") or entry.get("displayName") or entry.get("comment") or f"Lore {index + 1}")
        keys = entry.get("keys") or entry.get("key") or entry.get("keywords") or []
        if isinstance(keys, str):
            keys = [part.strip() for part in keys.split(",") if part.strip()]
        content = entry.get("content") or entry.get("text") or ""
        world["lore_cards"].append({
            "id": unique_slug(title, used),
            "type": "lore",
            "title": title,
            "content": content,
            "keywords": keys,
            "importance": 3,
            "extensions": {"source_entry": {k: v for k, v in entry.items() if k not in {"content", "text"}}},
        })
    return world


def main():
    parser = argparse.ArgumentParser(description="Convert generic/SillyTavern/NovelAI-like lorebook JSON.")
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    write_json(args.output, convert(load_json(args.input)))
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
