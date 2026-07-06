#!/usr/bin/env python3
import argparse
from loreweaver_common import empty_world, load_json, unique_slug, write_json


TYPE_MAP = {
    "character": "character",
    "location": "location",
    "faction": "faction",
    "item": "item",
    "event": "event",
    "rule": "world_rule",
    "world rule": "world_rule",
}


def convert(source):
    world = empty_world()
    world.update({
        "title": source.get("title", ""),
        "description": source.get("description", ""),
        "premise": source.get("backstory", ""),
        "opening": (source.get("greetings") or [""])[0],
        "style_rules": [source["custom_instructions"]] if source.get("custom_instructions") else [],
        "tags": source.get("tags", []),
        "visibility": "public" if source.get("settings", {}).get("public_scenario") else "private",
        "cover": source.get("cover_image"),
        "source": {"format": "fictionlab-scenario", "conversion_warnings": []},
    })
    used = set()
    name_to_id = {}
    for lore in source.get("lore", []):
        name = str(lore.get("name", "")).strip() or "Untitled lore"
        card_id = unique_slug(name, used)
        name_to_id[name.casefold()] = card_id
        raw_type = str(lore.get("type", "lore")).strip().casefold()
        content = str(lore.get("content", "")).strip()
        summary = str(lore.get("summary", "")).strip()
        world["lore_cards"].append({
            "id": card_id,
            "type": TYPE_MAP.get(raw_type, "lore"),
            "title": name,
            "content": content or summary,
            "keywords": [name] + ([summary] if summary and len(summary) <= 80 else []),
            "importance": lore.get("priority", 3),
            "image": lore.get("image"),
            "extensions": {"fictionlab_type": lore.get("type")} if raw_type not in TYPE_MAP else {},
        })
    forced = source.get("settings", {}).get("force_character")
    if forced and forced.casefold() in name_to_id:
        world["featured_character"] = name_to_id[forced.casefold()]
    world["settings"]["separate_user_character"] = source.get("settings", {}).get("separate_user_character")
    world["settings"]["allow_story_customization"] = source.get("settings", {}).get("allow_story_customization")
    world["settings"]["allow_commenting"] = source.get("settings", {}).get("allow_commenting")
    world["extensions"]["fictionlab"] = {
        "language": source.get("language"),
        "custom_lore_types": source.get("custom_lore_types", []),
        "hide_scenario_prompts": source.get("settings", {}).get("hide_scenario_prompts"),
    }
    return world


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    write_json(args.output, convert(load_json(args.input)))
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
