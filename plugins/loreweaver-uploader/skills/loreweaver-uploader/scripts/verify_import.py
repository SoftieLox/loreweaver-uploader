#!/usr/bin/env python3
import json
import sys
from collections import Counter
from loreweaver_common import load_json, normalize_world


def main():
    if len(sys.argv) != 3:
        print("usage: verify_import.py <expected-world.json> <observed-import.json>")
        return 2
    expected = normalize_world(load_json(sys.argv[1]))
    observed = load_json(sys.argv[2])
    expected_counts = {
        "lore_cards": len(expected["lore_cards"]),
        "relationships": len(expected["relationships"]),
        "loom_threads": len(expected["loom"]["threads"]),
        "quests": len(expected["loom"]["quests"]),
        "inventory": len(expected["loom"]["inventory"]),
    }
    errors = []
    for key, value in expected_counts.items():
        actual = observed.get("counts", {}).get(key)
        if actual is None:
            errors.append(f"observed counts missing {key}")
        elif actual != value:
            errors.append(f"{key}: expected {value}, observed {actual}")
    expected_types = Counter(c.get("type", "lore") for c in expected["lore_cards"] if isinstance(c, dict))
    observed_types = observed.get("counts", {}).get("by_type", {})
    if observed_types and dict(expected_types) != observed_types:
        errors.append(f"lore card type counts differ: expected {dict(expected_types)}, observed {observed_types}")
    observed_ids = set(observed.get("sample_card_ids", []))
    expected_ids = {c.get("id") for c in expected["lore_cards"] if isinstance(c, dict)}
    missing_samples = observed_ids - expected_ids
    if missing_samples:
        errors.append(f"observed sample IDs are not in expected package: {sorted(missing_samples)}")
    result = {"expected_counts": expected_counts, "errors": errors, "verified": not errors}
    print(json.dumps(result, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
