# Loom Engine authoring

LoreWeaver publicly describes Loom as IF/THEN narrative scripting evaluated during play. Live controls are authoritative.

For each thread record:

- name and intent;
- enabled state;
- trigger;
- conditions;
- actions in order;
- once/repeat/cooldown behavior;
- priority or conflict policy;
- state read and written;
- priority from 0–100, tags, visibility, cooldown, and maximum fire count;
- one positive and one negative test.

Use explicit, observable conditions. Prefer a state flag over repeatedly matching ambiguous prose. Make actions idempotent when they may run more than once.

Check for:

- unreachable conditions;
- actions referencing missing cards, variables, quests, or items;
- loops where an action immediately retriggers itself;
- two threads writing incompatible values in the same turn;
- one-time rewards without a consumed/complete flag;
- HUD values without bounds;
- quests with no completion transition.

Never paste an invented JSON shape directly into LoreWeaver. Map the normalized design to controls observed in the live Loom editor or to a verified exported format.

## Verified live surfaces (July 6, 2026)

The authenticated editor currently exposes:

- thread search, New, Templates, Manage, import, and export;
- a Story World State toggle;
- IF, THEN, and Settings tabs;
- thread enabled/disabled state and description;
- priority slider, tags, repeat/one-shot behavior, visibility, cooldown, and maximum fires;
- 43 templates, including Health System, Leveling & XP, Mana & Spellcasting, Alignment & Karma, and Quest Tracker;
- condition summaries such as always-active flags, message keywords, chance, turn intervals, and lore triggers;
- actions such as narrative/environment injection and numeric state changes.

`New` is an immediate external write. Never click it merely to inspect the editor.
