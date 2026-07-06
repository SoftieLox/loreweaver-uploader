#!/usr/bin/env python3
"""Heuristic lore-quality analysis. Findings require human review."""

import json
import re
import sys
from collections import Counter, defaultdict, deque
from loreweaver_common import GENERIC_KEYWORDS, load_json, normalize_world


NEGATIONS = {"not", "never", "no", "cannot", "can't", "isn't", "wasn't", "without"}


def words(text):
    return {
        token for token in re.findall(r"[a-z0-9']+", text.casefold())
        if len(token) > 2 and token not in {"the", "and", "that", "with", "from", "this", "into", "their"}
    }


def sentences(text):
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if len(part.strip()) >= 18]


def main():
    if len(sys.argv) != 2:
        print("usage: analyze_lore.py <world.json>")
        return 2
    world = normalize_world(load_json(sys.argv[1]))
    cards = [card for card in world["lore_cards"] if isinstance(card, dict)]
    findings = []

    sentence_rows = []
    for card in cards:
        for sentence in sentences(str(card.get("content", ""))):
            token_set = words(sentence)
            sentence_rows.append((card.get("id"), sentence, token_set, bool(token_set & NEGATIONS)))
    for index, left in enumerate(sentence_rows):
        for right in sentence_rows[index + 1:]:
            if left[0] == right[0] or min(len(left[2]), len(right[2])) < 4:
                continue
            overlap = len(left[2] & right[2]) / max(1, len(left[2] | right[2]))
            if overlap >= 0.45 and left[3] != right[3]:
                findings.append({
                    "severity": "review",
                    "kind": "possible_contradiction",
                    "cards": [left[0], right[0]],
                    "sentences": [left[1], right[1]],
                    "reason": "high lexical overlap with different negation",
                })

    adjacency = defaultdict(set)
    indegree = Counter()
    for relation in world["relationships"]:
        if not isinstance(relation, dict):
            continue
        source, target = relation.get("from"), relation.get("to")
        if source and target:
            adjacency[source].add(target)
            adjacency[target].add(source)
            indegree[source] += 1
            indegree[target] += 1
    ids = {card.get("id") for card in cards}
    components = []
    unseen = set(ids)
    while unseen:
        start = unseen.pop()
        component = {start}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        components.append(sorted(component))
    if len(components) > 1 and len(ids) > 1:
        findings.append({
            "severity": "warning",
            "kind": "disconnected_lore_graph",
            "components": sorted(components, key=len, reverse=True),
        })

    keyword_counts = Counter()
    for card in cards:
        for keyword in card.get("keywords", []) if isinstance(card.get("keywords", []), list) else []:
            keyword_counts[str(keyword).strip().casefold()] += 1
    for keyword, count in keyword_counts.items():
        if keyword in GENERIC_KEYWORDS or count >= 4:
            findings.append({
                "severity": "warning",
                "kind": "weak_keyword",
                "keyword": keyword,
                "card_count": count,
            })

    hubs = [{"id": card_id, "degree": degree} for card_id, degree in indegree.most_common() if degree >= 5]
    result = {
        "title": world["title"],
        "cards": len(cards),
        "relationships": len(world["relationships"]),
        "components": len(components),
        "hubs": hubs,
        "findings": findings,
        "note": "Contradiction findings are heuristic and must be reviewed; they are not automatic rewrite instructions.",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
