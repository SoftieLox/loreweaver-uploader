#!/usr/bin/env python3
import json
import sys
from loreweaver_common import load_json, normalize_world


def main():
    if len(sys.argv) != 2:
        print("usage: build_playtest_plan.py <world.json>")
        return 2
    world = normalize_world(load_json(sys.argv[1]))
    tests = [{
        "id": "opening-agency",
        "purpose": "Opening establishes pressure without choosing for the player.",
        "setup": world["opening"],
        "assert": ["player has an actionable choice", "premise and opening agree"],
    }]
    for card in world["lore_cards"]:
        if isinstance(card, dict) and (card.get("importance", 3) >= 4 or card.get("pinned")):
            tests.append({
                "id": f"lore-{card.get('id')}",
                "purpose": f"Critical lore retrieval for {card.get('title')}.",
                "prompt": f"Naturally mention or interact with {card.get('title')} without quoting its card.",
                "assert": ["canonical facts preserved", "no unrelated lore leakage"],
            })
    for thread in world["loom"]["threads"]:
        if not isinstance(thread, dict):
            continue
        tests.append({
            "id": f"loom-{thread.get('id')}-positive",
            "purpose": "Verify the Loom thread fires when its conditions are satisfied.",
            "conditions": thread.get("conditions", []),
            "assert": thread.get("actions", []),
        })
        tests.append({
            "id": f"loom-{thread.get('id')}-negative",
            "purpose": "Verify the Loom thread does not fire before its conditions are satisfied.",
            "conditions": {"negate": thread.get("conditions", [])},
            "assert_not": thread.get("actions", []),
        })
    print(json.dumps({"title": world["title"], "test_count": len(tests), "tests": tests}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
