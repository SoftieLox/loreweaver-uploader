# Portable world package

This is a plugin-owned interchange format, not a claim about LoreWeaver's private API.

```json
{
  "schema_version": "0.2",
  "mode": "world",
  "title": "Required",
  "description": "",
  "premise": "Required",
  "opening": "",
  "tone": [],
  "style_rules": [],
  "player_context": "",
  "genres": [],
  "tags": [],
  "content_rating": null,
  "visibility": "private",
  "cover": null,
  "featured_character": null,
  "lore_cards": [
    {
      "id": "stable-slug",
      "type": "character",
      "title": "Required",
      "content": "Required",
      "keywords": [],
      "tags": [],
      "importance": 3,
      "pinned": false,
      "prompt_active": true,
      "private": false,
      "image": null,
      "private_notes": null
    }
  ],
  "relationships": [
    {
      "from": "stable-slug",
      "to": "other-slug",
      "label": "member of",
      "description": ""
    }
  ],
  "loom": {
    "variables": [
      {
        "name": "trust",
        "type": "integer",
        "minimum": 0,
        "maximum": 5,
        "initial": 1
      }
    ],
    "threads": [
      {
        "id": "reveal-secret",
        "name": "Reveal the secret",
        "conditions": [],
        "actions": [],
        "repeat": "once",
        "priority": 50,
        "visible": true,
        "cooldown": null,
        "max_fires": null,
        "tags": [],
        "tests": []
      }
    ],
    "quests": [],
    "inventory": [],
    "hud": {}
  },
  "settings": {},
  "source": {},
  "extensions": {},
  "creator_notes": ""
}
```

Rules:

- `mode` is `world` or `character`.
- `visibility` is `private`, `unlisted`, or `public`; verify live availability.
- Card IDs are unique lowercase slugs and remain stable across updates.
- Importance is an integer from 1 through 5.
- Native lore types currently visible in the authenticated editor are Character, Location, Faction, Item, Event/History, and Misc. Portable aliases must be mapped explicitly.
- `pinned`, `prompt_active`, and `private` preserve live lore behavior where supported.
- `tags` preserves native LoreWeaver tags; `keywords` remains authoring/retrieval metadata for cross-platform conversions. When exporting native lore and `tags` is empty, the converter falls back to `keywords`.
- Relationship endpoints refer to card IDs.
- `featured_character` refers to a character card ID and is required in character mode.
- Loom variable and entity identifiers are lowercase slugs.
- Use `extensions` to preserve unmapped source fields. Never silently discard them.
- `private_notes` and `creator_notes` are excluded from publication unless the user explicitly maps them to a live field.
- Unknown live fields go in a clearly named extension object only after inspection; never silently discard them.

This is the plugin's stable interchange format. It is deliberately separate from LoreWeaver's native export format until a real export has been structurally verified.
