# Verified LoreWeaver native lore JSON

Verified from an authentic export supplied on July 6, 2026.

The file is a top-level JSON array. Each entry has exactly:

```json
{
  "title": "Mara Venn",
  "type": "character",
  "description": "Card content",
  "tags": ["Mara", "cartographer"],
  "importance": 5,
  "pinned": true,
  "activeForPrompt": true,
  "image": null
}
```

Observed native types:

- `character`
- `location`
- `faction`
- `item` (exposed by the live editor and importer; absent from the supplied sample)
- `event`
- `misc`

Importance is an integer from 1 through 5. `pinned` and `activeForPrompt` are booleans. `tags` is an array of strings. `image` may be null; non-null image representation remains unverified.

Native lore exports do not contain world title, premise, relationships, Loom threads, or portable card IDs. Importing into the portable package therefore requires a title, generates IDs from card titles, and cannot manufacture relationships.

Use:

```text
import_native_lore.py lore-export.json world.json --title "World title"
export_native_lore.py world.json lore-export.json
```

The native exporter maps portable `event_history` to `event`, and portable `concept`, `lore`, and `world_rule` to `misc`.
