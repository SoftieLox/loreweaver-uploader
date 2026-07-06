#!/usr/bin/env python3
import argparse
from loreweaver_common import load_json, normalize_world, write_json


def main():
    parser = argparse.ArgumentParser(description="Create a reviewable public copy without private metadata.")
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    world = normalize_world(load_json(args.input))
    world["creator_notes"] = ""
    world["source"] = {}
    world["extensions"] = {}
    public_cards = []
    removed = []
    for card in world["lore_cards"]:
        if not isinstance(card, dict):
            continue
        if card.get("private"):
            removed.append(card.get("id"))
            continue
        card = dict(card)
        card.pop("private_notes", None)
        card.pop("extensions", None)
        public_cards.append(card)
    public_ids = {card.get("id") for card in public_cards}
    world["lore_cards"] = public_cards
    world["relationships"] = [
        relation for relation in world["relationships"]
        if isinstance(relation, dict)
        and relation.get("from") in public_ids
        and relation.get("to") in public_ids
    ]
    world["visibility"] = "private"
    world["extensions"] = {"publication_preparation": {"removed_private_card_ids": removed}}
    write_json(args.output, world)
    print(f"{args.output}\nRemoved {len(removed)} private card(s). Visibility remains private pending review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
