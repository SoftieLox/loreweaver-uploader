#!/usr/bin/env python3
import argparse
from loreweaver_common import empty_world, load_json, unique_slug, write_json


def entry_content(entry):
    return entry.get("content") or entry.get("text") or entry.get("description") or ""


def convert(source):
    data = source.get("data", source)
    name = str(data.get("name", "")).strip() or "Imported Character"
    world = empty_world()
    world["mode"] = "character"
    world["title"] = name
    world["description"] = data.get("creator_notes", "")[:500]
    world["premise"] = data.get("scenario") or data.get("description") or f"A character experience featuring {name}."
    world["opening"] = data.get("first_mes", "")
    world["style_rules"] = [data["system_prompt"]] if data.get("system_prompt") else []
    world["tags"] = data.get("tags", [])
    world["visibility"] = "private"
    world["source"] = {"format": source.get("spec", "character-card")}
    used = set()
    character_id = unique_slug(name, used)
    sections = [
        ("Description", data.get("description")),
        ("Personality", data.get("personality")),
        ("Dialogue examples", data.get("mes_example")),
    ]
    character_content = "\n\n".join(f"{title}:\n{text}" for title, text in sections if text)
    world["lore_cards"].append({
        "id": character_id,
        "type": "character",
        "title": name,
        "content": character_content or world["premise"],
        "keywords": [name],
        "importance": 5,
        "image": None,
    })
    world["featured_character"] = character_id
    book = data.get("character_book") or data.get("characterBook") or {}
    entries = book.get("entries", []) if isinstance(book, dict) else []
    for entry in entries:
        title = str(entry.get("name") or entry.get("comment") or entry.get("title") or "Lore").strip()
        card_id = unique_slug(title, used)
        keys = entry.get("keys") or entry.get("key") or entry.get("keywords") or []
        if isinstance(keys, str):
            keys = [part.strip() for part in keys.split(",") if part.strip()]
        priority = entry.get("priority", 3)
        if not isinstance(priority, int) or not 1 <= priority <= 5:
            priority = 3
        world["lore_cards"].append({
            "id": card_id,
            "type": "lore",
            "title": title,
            "content": entry_content(entry),
            "keywords": keys,
            "importance": priority,
            "extensions": {"source_entry": {k: v for k, v in entry.items() if k not in {"content", "text"}}},
        })
    return world


def main():
    parser = argparse.ArgumentParser(description="Convert Character Card V2/V3 or SillyTavern JSON.")
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    write_json(args.output, convert(load_json(args.input)))
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
