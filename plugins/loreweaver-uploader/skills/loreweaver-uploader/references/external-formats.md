# External format conversion

Converters produce the stable portable package from:

- FictionLab normalized scenario JSON;
- Character Card V2/V3-style JSON and SillyTavern character exports;
- generic, SillyTavern-like, and NovelAI-like lorebook JSON.

Conversions are conservative:

- visibility defaults to private unless the source explicitly says public;
- unmapped source fields are retained under `extensions`;
- source-specific metadata is never treated as a verified LoreWeaver field;
- no converter publishes or uploads;
- converted packages must pass `validate_world.py` before browser use.

LoreWeaver native lore and Loom JSON are now verified. Read `native-lore-format.md` and `native-loom-format.md`, then use the corresponding import/export scripts. Full-world LoreWeaver JSON remains distinct and should still be probed before adding a full-world converter.

## Verified native import routes

The authenticated UI currently advertises:

- World import: LoreWeaver JSON (full), AI Dungeon ZIP export (full), FictionLab JSON export (best effort), and NovelAI `.story` (best effort).
- Lore import: LoreWeaver JSON lore export (full), AI Dungeon story cards JSON (full), and NovelAI `.lorebook` (best effort).

World import may include worlds, lore, and story sessions. FictionLab mapping may include scenario details, player-character information, and chat history. NovelAI mapping prioritizes metadata, lorebook, and generation settings when packed history is unavailable.

Prefer the site's full native importer for supported exact formats. Use plugin converters when the user needs reviewable normalization, cross-format editing, validation, or a format LoreWeaver does not directly accept.
