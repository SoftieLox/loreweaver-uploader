#!/usr/bin/env python3
import json
import sys
from loreweaver_common import load_json, normalize_world


def estimate_tokens(text):
    return max(1, round(len(text) / 4)) if text else 0


def main():
    if len(sys.argv) != 2:
        print("usage: estimate_context.py <world.json>")
        return 2
    world = normalize_world(load_json(sys.argv[1]))
    foundation = "\n".join([
        world["premise"], world["opening"], world["player_context"],
        *world["tone"], *world["style_rules"],
    ])
    cards = []
    for card in world["lore_cards"]:
        if not isinstance(card, dict):
            continue
        text = f"{card.get('title', '')}\n{card.get('content', '')}\n{' '.join(card.get('keywords', []))}"
        cards.append({
            "id": card.get("id"),
            "importance": card.get("importance", 3),
            "estimated_tokens": estimate_tokens(text),
            "pinned": bool(card.get("pinned")),
            "prompt_active": card.get("prompt_active", True),
        })
    active = [card for card in cards if card["prompt_active"]]
    report = {
        "foundation_estimated_tokens": estimate_tokens(foundation),
        "active_lore_estimated_tokens": sum(card["estimated_tokens"] for card in active),
        "pinned_lore_estimated_tokens": sum(card["estimated_tokens"] for card in active if card["pinned"]),
        "importance_5_estimated_tokens": sum(card["estimated_tokens"] for card in active if card["importance"] == 5),
        "largest_cards": sorted(active, key=lambda card: card["estimated_tokens"], reverse=True)[:10],
        "note": "Character-based estimates are approximate; LoreWeaver controls actual retrieval and context allocation.",
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
