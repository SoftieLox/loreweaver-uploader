#!/usr/bin/env python3
"""Shared, dependency-free helpers for LoreWeaver package tooling."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any

CARD_TYPES = {
    "character", "location", "faction", "item", "event_history", "misc",
    "event", "concept", "lore", "world_rule",
}
VISIBILITIES = {"private", "unlisted", "public"}
MODES = {"world", "character"}
RATINGS = {"everyone", "teen", "mature", None}
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*$")
GENERIC_KEYWORDS = {"the", "a", "an", "it", "they", "world", "character", "location", "thing"}


def load_json(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("top-level JSON value must be an object")
    return data


def write_json(path: str | Path, data: Any) -> None:
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def slugify(value: str, fallback: str = "entry") -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or fallback


def unique_slug(value: str, used: set[str]) -> str:
    base = slugify(value)
    candidate = base
    number = 2
    while candidate in used:
        candidate = f"{base}-{number}"
        number += 1
    used.add(candidate)
    return candidate


def empty_world() -> dict[str, Any]:
    return {
        "schema_version": "0.2",
        "mode": "world",
        "title": "",
        "description": "",
        "premise": "",
        "opening": "",
        "tone": [],
        "style_rules": [],
        "player_context": "",
        "genres": [],
        "tags": [],
        "content_rating": None,
        "visibility": "private",
        "cover": None,
        "featured_character": None,
        "lore_cards": [],
        "relationships": [],
        "loom": {
            "variables": [],
            "threads": [],
            "quests": [],
            "inventory": [],
            "hud": {},
        },
        "settings": {},
        "source": {},
        "extensions": {},
        "creator_notes": "",
    }


def normalize_world(data: dict[str, Any]) -> dict[str, Any]:
    result = empty_world()
    for key in result:
        if key in data:
            result[key] = copy.deepcopy(data[key])
    result["schema_version"] = str(data.get("schema_version", "0.2"))
    for key in ("tone", "style_rules", "genres", "tags", "lore_cards", "relationships"):
        if not isinstance(result[key], list):
            result[key] = []
    if not isinstance(result["loom"], dict):
        result["loom"] = {}
    for key, default in (("variables", []), ("threads", []), ("quests", []), ("inventory", []), ("hud", {})):
        result["loom"].setdefault(key, copy.deepcopy(default))
    result["settings"] = result["settings"] if isinstance(result["settings"], dict) else {}
    result["source"] = result["source"] if isinstance(result["source"], dict) else {}
    result["extensions"] = result["extensions"] if isinstance(result["extensions"], dict) else {}
    return result


def validate_world(data: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []
    world = normalize_world(data)

    if world["schema_version"] not in {"0.1", "0.2"}:
        warnings.append(f"unrecognized schema_version {world['schema_version']!r}")
    if world["mode"] not in MODES:
        errors.append("mode must be 'world' or 'character'")
    for field in ("title", "premise"):
        if not isinstance(world[field], str) or not world[field].strip():
            errors.append(f"{field} is required")
    if world["visibility"] not in VISIBILITIES:
        errors.append("visibility must be private, unlisted, or public")
    rating = world["content_rating"]
    normalized_rating = rating.lower() if isinstance(rating, str) else rating
    if normalized_rating not in RATINGS:
        errors.append("content_rating must be Everyone, Teen, Mature, or null")
    if world["visibility"] == "public" and rating is None:
        errors.append("public packages require a content_rating")

    cards = world["lore_cards"]
    ids: set[str] = set()
    titles: dict[str, str] = {}
    contents: dict[str, str] = {}
    keyword_owners: dict[str, set[str]] = {}
    importance_fives = 0
    for index, card in enumerate(cards):
        prefix = f"lore_cards[{index}]"
        if not isinstance(card, dict):
            errors.append(f"{prefix} must be an object")
            continue
        card_id = card.get("id")
        if not isinstance(card_id, str) or not SLUG.fullmatch(card_id):
            errors.append(f"{prefix}.id must be a lowercase slug")
        elif card_id in ids:
            errors.append(f"duplicate lore card id: {card_id}")
        else:
            ids.add(card_id)
        title = str(card.get("title", "")).strip()
        if not title:
            errors.append(f"{prefix}.title is required")
        elif title.casefold() in titles:
            errors.append(f"duplicate lore card title (case-insensitive): {title}")
        else:
            titles[title.casefold()] = card_id or prefix
        content = str(card.get("content", "")).strip()
        if not content:
            errors.append(f"{prefix}.content is required")
        elif re.sub(r"\s+", " ", content).casefold() in contents:
            warnings.append(f"{prefix}.content duplicates another lore card")
        else:
            contents[re.sub(r"\s+", " ", content).casefold()] = card_id or prefix
        card_type = card.get("type", "lore")
        if card_type not in CARD_TYPES:
            warnings.append(f"{prefix}.type {card_type!r} is not a known portable type")
        for flag in ("pinned", "prompt_active", "private"):
            if flag in card and not isinstance(card[flag], bool):
                errors.append(f"{prefix}.{flag} must be boolean")
        importance = card.get("importance", 3)
        if not isinstance(importance, int) or isinstance(importance, bool) or not 1 <= importance <= 5:
            errors.append(f"{prefix}.importance must be an integer from 1 to 5")
        elif importance == 5:
            importance_fives += 1
        keywords = card.get("keywords", [])
        if not isinstance(keywords, list) or any(not isinstance(x, str) for x in keywords):
            errors.append(f"{prefix}.keywords must be an array of strings")
        else:
            normalized = [x.strip().casefold() for x in keywords if x.strip()]
            if len(normalized) != len(set(normalized)):
                warnings.append(f"{prefix}.keywords contains duplicates")
            for keyword in normalized:
                keyword_owners.setdefault(keyword, set()).add(card_id or prefix)
                if keyword in GENERIC_KEYWORDS:
                    warnings.append(f"{prefix}.keyword {keyword!r} is too generic for reliable retrieval")
        tags = card.get("tags", [])
        if not isinstance(tags, list) or any(not isinstance(x, str) for x in tags):
            errors.append(f"{prefix}.tags must be an array of strings")
        if world["visibility"] == "public" and card.get("private_notes"):
            warnings.append(f"{prefix}.private_notes must remain excluded from publication")

    relation_keys: set[tuple[str, str, str]] = set()
    connected: set[str] = set()
    for index, relation in enumerate(world["relationships"]):
        prefix = f"relationships[{index}]"
        if not isinstance(relation, dict):
            errors.append(f"{prefix} must be an object")
            continue
        source = relation.get("from")
        target = relation.get("to")
        label = str(relation.get("label", "")).strip()
        if source not in ids:
            errors.append(f"{prefix}.from references a missing card")
        if target not in ids:
            errors.append(f"{prefix}.to references a missing card")
        if not label:
            errors.append(f"{prefix}.label is required")
        if source == target and source in ids:
            warnings.append(f"{prefix} is a self-relationship")
        key = (str(source), str(target), label.casefold())
        if key in relation_keys:
            warnings.append(f"{prefix} duplicates another relationship")
        relation_keys.add(key)
        connected.update(x for x in (source, target) if x in ids)

    if len(cards) > 1:
        orphaned = sorted(ids - connected)
        if orphaned:
            preview = ", ".join(orphaned[:20])
            suffix = f", and {len(orphaned) - 20} more" if len(orphaned) > 20 else ""
            warnings.append(
                f"{len(orphaned)} orphan lore card(s) with no relationships: {preview}{suffix}"
            )
    if cards and importance_fives / len(cards) > 0.35:
        warnings.append("more than 35% of lore cards are importance 5; critical context is overcrowded")
    for keyword, owners in sorted(keyword_owners.items()):
        if len(owners) >= 4:
            warnings.append(f"keyword {keyword!r} is shared by {len(owners)} cards and may retrieve too broadly")

    if world["mode"] == "character":
        featured = world["featured_character"]
        if not featured:
            errors.append("character mode requires featured_character")
        elif featured not in ids:
            errors.append("featured_character must reference an existing lore card id")
        else:
            featured_card = next((c for c in cards if isinstance(c, dict) and c.get("id") == featured), {})
            if featured_card.get("type") != "character":
                errors.append("featured_character must reference a character lore card")

    loom = world["loom"]
    variables = loom.get("variables", [])
    variable_names: set[str] = set()
    if not isinstance(variables, list):
        errors.append("loom.variables must be an array")
        variables = []
    for index, variable in enumerate(variables):
        prefix = f"loom.variables[{index}]"
        if not isinstance(variable, dict):
            errors.append(f"{prefix} must be an object")
            continue
        name = variable.get("name")
        if not isinstance(name, str) or not SLUG.fullmatch(name):
            errors.append(f"{prefix}.name must be a lowercase slug")
        elif name in variable_names:
            errors.append(f"duplicate Loom variable: {name}")
        else:
            variable_names.add(name)
        vtype = variable.get("type")
        if vtype not in {"boolean", "integer", "number", "string"}:
            errors.append(f"{prefix}.type must be boolean, integer, number, or string")
        if vtype in {"integer", "number"}:
            minimum, maximum, initial = variable.get("minimum"), variable.get("maximum"), variable.get("initial")
            if minimum is not None and maximum is not None and minimum > maximum:
                errors.append(f"{prefix} minimum exceeds maximum")
            if initial is not None and minimum is not None and initial < minimum:
                errors.append(f"{prefix}.initial is below minimum")
            if initial is not None and maximum is not None and initial > maximum:
                errors.append(f"{prefix}.initial is above maximum")

    threads = loom.get("threads", [])
    thread_ids: set[str] = set()
    if not isinstance(threads, list):
        errors.append("loom.threads must be an array")
        threads = []
    for index, thread in enumerate(threads):
        prefix = f"loom.threads[{index}]"
        if not isinstance(thread, dict):
            errors.append(f"{prefix} must be an object")
            continue
        thread_id = thread.get("id")
        if not isinstance(thread_id, str) or not SLUG.fullmatch(thread_id):
            errors.append(f"{prefix}.id must be a lowercase slug")
        elif thread_id in thread_ids:
            errors.append(f"duplicate Loom thread id: {thread_id}")
        else:
            thread_ids.add(thread_id)
        conditions = thread.get("conditions", [])
        actions = thread.get("actions", [])
        if not isinstance(conditions, list) or not conditions:
            warnings.append(f"{prefix} has no explicit conditions")
        if not isinstance(actions, list) or not actions:
            errors.append(f"{prefix} requires at least one action")
            actions = []
        for section, entries in (("conditions", conditions), ("actions", actions)):
            if not isinstance(entries, list):
                continue
            for item_index, item in enumerate(entries):
                if not isinstance(item, dict):
                    errors.append(f"{prefix}.{section}[{item_index}] must be an object")
                    continue
                variable = item.get("variable")
                if variable and variable not in variable_names:
                    errors.append(f"{prefix}.{section}[{item_index}] references missing variable {variable!r}")
                target = item.get("target")
                target_kind = item.get("target_kind")
                if target_kind == "lore_card" and target not in ids:
                    errors.append(f"{prefix}.{section}[{item_index}] references missing lore card {target!r}")
        if thread.get("repeat") not in {None, "once", "repeat", "cooldown"}:
            errors.append(f"{prefix}.repeat must be once, repeat, or cooldown")
        priority = thread.get("priority")
        if priority is not None and (not isinstance(priority, int) or isinstance(priority, bool) or not 0 <= priority <= 100):
            errors.append(f"{prefix}.priority must be an integer from 0 to 100")
        for number_field in ("cooldown", "max_fires"):
            value = thread.get(number_field)
            if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
                errors.append(f"{prefix}.{number_field} must be a non-negative integer or null")
        if thread.get("repeat") == "repeat":
            condition_vars = {x.get("variable") for x in conditions if isinstance(x, dict)}
            action_vars = {x.get("variable") for x in actions if isinstance(x, dict)}
            if condition_vars & action_vars and not thread.get("cooldown"):
                warnings.append(f"{prefix} may immediately retrigger after writing its own condition state")

    quests = loom.get("quests", [])
    quest_ids: set[str] = set()
    if not isinstance(quests, list):
        errors.append("loom.quests must be an array")
        quests = []
    for index, quest in enumerate(quests):
        prefix = f"loom.quests[{index}]"
        if not isinstance(quest, dict):
            errors.append(f"{prefix} must be an object")
            continue
        quest_id = quest.get("id")
        if not isinstance(quest_id, str) or not SLUG.fullmatch(quest_id):
            errors.append(f"{prefix}.id must be a lowercase slug")
        elif quest_id in quest_ids:
            errors.append(f"duplicate quest id: {quest_id}")
        else:
            quest_ids.add(quest_id)
        if not quest.get("completion"):
            warnings.append(f"{prefix} has no completion transition")

    inventory = loom.get("inventory", [])
    item_ids: set[str] = set()
    if not isinstance(inventory, list):
        errors.append("loom.inventory must be an array")
        inventory = []
    for index, item in enumerate(inventory):
        prefix = f"loom.inventory[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not SLUG.fullmatch(item_id):
            errors.append(f"{prefix}.id must be a lowercase slug")
        elif item_id in item_ids:
            errors.append(f"duplicate inventory item id: {item_id}")
        else:
            item_ids.add(item_id)

    if world["visibility"] == "public":
        warnings.append("public visibility requires action-time confirmation and guideline review")
        if world.get("creator_notes"):
            warnings.append("creator_notes must remain excluded from publication")
    info.append(
        f"{len(cards)} lore card(s), {len(world['relationships'])} relationship(s), "
        f"{len(threads)} Loom thread(s)"
    )
    return errors, warnings, info


def keyed_map(items: Any, key_fields: tuple[str, ...]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    if not isinstance(items, list):
        return result
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            result[f"#{index}"] = item
            continue
        key = "|".join(str(item.get(field, "")) for field in key_fields)
        result[key or f"#{index}"] = item
    return result


def diff_worlds(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    old = normalize_world(before)
    new = normalize_world(after)
    result: dict[str, Any] = {"fields": {}, "collections": {}}
    for field in (
        "mode", "title", "description", "premise", "opening", "tone", "style_rules",
        "player_context", "genres", "tags", "content_rating", "visibility", "cover",
        "featured_character", "settings",
    ):
        if old.get(field) != new.get(field):
            result["fields"][field] = {"before": old.get(field), "after": new.get(field)}
    specs = {
        "lore_cards": (old["lore_cards"], new["lore_cards"], ("id",)),
        "relationships": (old["relationships"], new["relationships"], ("from", "to", "label")),
        "loom.variables": (old["loom"].get("variables"), new["loom"].get("variables"), ("name",)),
        "loom.threads": (old["loom"].get("threads"), new["loom"].get("threads"), ("id",)),
        "loom.quests": (old["loom"].get("quests"), new["loom"].get("quests"), ("id",)),
        "loom.inventory": (old["loom"].get("inventory"), new["loom"].get("inventory"), ("id",)),
    }
    for name, (before_items, after_items, keys) in specs.items():
        before_map = keyed_map(before_items, keys)
        after_map = keyed_map(after_items, keys)
        added = {key: after_map[key] for key in after_map.keys() - before_map.keys()}
        removed = {key: before_map[key] for key in before_map.keys() - after_map.keys()}
        modified = {
            key: {"before": before_map[key], "after": after_map[key]}
            for key in before_map.keys() & after_map.keys()
            if before_map[key] != after_map[key]
        }
        if added or removed or modified:
            result["collections"][name] = {"added": added, "removed": removed, "modified": modified}
    result["summary"] = {
        "field_changes": len(result["fields"]),
        "collections_changed": len(result["collections"]),
        "added": sum(len(v["added"]) for v in result["collections"].values()),
        "removed": sum(len(v["removed"]) for v in result["collections"].values()),
        "modified": sum(len(v["modified"]) for v in result["collections"].values()),
    }
    return result
