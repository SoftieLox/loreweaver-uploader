#!/usr/bin/env python3
import json
import sys
from collections import Counter
from loreweaver_common import load_json, normalize_world, validate_world


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: qa_report.py <world.json>")
        return 2
    world = normalize_world(load_json(sys.argv[1]))
    errors, warnings, info = validate_world(world)
    types = Counter(card.get("type", "lore") for card in world["lore_cards"] if isinstance(card, dict))
    report = {
        "title": world["title"],
        "mode": world["mode"],
        "visibility": world["visibility"],
        "content_rating": world["content_rating"],
        "counts": {
            "lore_cards": len(world["lore_cards"]),
            "by_type": dict(sorted(types.items())),
            "relationships": len(world["relationships"]),
            "loom_variables": len(world["loom"]["variables"]),
            "loom_threads": len(world["loom"]["threads"]),
            "quests": len(world["loom"]["quests"]),
            "inventory": len(world["loom"]["inventory"]),
        },
        "errors": errors,
        "warnings": warnings,
        "info": info,
        "ready_for_private_draft": not errors,
        "ready_for_publication_review": not errors and world["content_rating"] is not None and bool(world["cover"]),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
