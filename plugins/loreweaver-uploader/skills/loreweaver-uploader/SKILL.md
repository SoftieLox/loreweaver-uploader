---
name: loreweaver-uploader
description: Design, develop, validate, import, create, update, playtest, draft, publish, export, or review LoreWeaver AI worlds and character experiences. Creates premises, typed lore cards, relationships, importance ratings, creator metadata, and Loom Engine rules, then packages them for loreweaverai.com.
---

# LoreWeaver World Publisher

Use the in-app browser-control skill because this workflow depends on the user's existing LoreWeaver login. Never request, read, expose, or store passwords, cookies, tokens, browser profiles, or local storage.

LoreWeaver changes frequently. Inspect the live creator before filling it, and treat visible labels, limits, requirements, and import formats as authoritative. The public Hub is `https://www.loreweaverai.com/hub`.

## Bundled resources

- Read `references/world-schema.md` before creating, importing, exporting, or validating a package.
- Read `references/world-design.md` when inventing or restructuring creative content.
- Read `references/loom-engine.md` for IF/THEN threads, HUD state, quests, inventory, conditions, and actions.
- Read `references/operations.md` for browser writes, imports, playtests, updates, publishing, and recovery.
- Read `references/external-formats.md` before converting or routing imports.
- Read `references/native-lore-format.md` before importing or exporting LoreWeaver-native lore JSON.
- Read `references/native-loom-format.md` before importing or exporting LoreWeaver-native Loom JSON.
- Read `references/publishing-checklist.md` before any Hub publication.
- Read `references/tooling.md` for script commands.
- Copy `assets/world-template.md` when the user wants a blank authoring worksheet.
- Run `scripts/validate_world.py <world.json>` before browser work when the source is JSON.
- Run `scripts/qa_report.py <world.json>` for a publication-readiness report.
- Run `scripts/analyze_lore.py <world.json>` for disconnected graphs, weak retrieval keywords, hubs, and possible canon contradictions. Treat contradiction results as review prompts, never automatic truth.
- Run `scripts/estimate_context.py <world.json>` to flag oversized pinned or critical lore before import.
- Run `scripts/build_playtest_plan.py <world.json>` to generate positive and negative tests for critical lore and Loom threads.
- Run `scripts/prepare_public_copy.py <input.json> <output.json>` to remove private cards and author metadata into a review copy. It deliberately leaves visibility private.
- Run `scripts/diff_world.py <current.json> <proposed.json>` before broad updates.
- Use `scripts/version_history.py` to snapshot, list, or restore package versions.
- Use `scripts/convert_fictionlab.py`, `scripts/convert_character_card.py`, or `scripts/convert_lorebook.py` for supported external formats.
- Use `scripts/import_native_lore.py` and `scripts/export_native_lore.py` for the verified LoreWeaver lore-array format. Do not describe it as a full-world export.
- Use `scripts/import_native_loom.py` and `scripts/export_native_loom.py` for verified Loom v1.0 JSON. Preserve unknown condition/action objects.
- Run `scripts/verify_import.py <expected.json> <observed.json>` after importing.
- Run `scripts/probe_export.py <export.json>` on an authentic LoreWeaver export before adding or changing native-format mappings.
- Read `references/ui-contract.json` before browser automation. If the authenticated contract is absent or stale, inspect first.
- Run `scripts/check_ui_contract.py` when the creator layout may have changed, and `scripts/record_ui_contract.py` only after a verified inspection.
- Run `scripts/run_fixture_tests.py` after changing converters, validation, diffing, or verification behavior.

## Creation modes

Support both:

- `world`: multi-character interactive setting or adventure;
- `character`: dedicated one-on-one character roleplay.

Do not convert one mode into the other by inference. A regular world can contain many character lore cards; a character experience has a different player fantasy and creator surface.

## Creative development

Before opening the creator, establish:

1. player fantasy, mode, genre, tone, boundaries, and desired scope;
2. premise, opening situation, player role, and unresolved central pressure;
3. tone and prose/style rules;
4. characters, locations, factions, items, events, concepts, and world rules;
5. relationships and importance ratings;
6. Loom Engine behavior, if any;
7. discoverability and publishing choices.

Preserve player agency. Do not prescribe the player's feelings, solve the central conflict in the setup, or mistake a wiki dump for an opening scene.

## Lore model

Normalize content into typed lore cards. Known public types include:

- character
- location
- faction
- item
- event
- lore or concept
- world rule

Each card should have a unique title, substantive content, optional tags/keywords, importance from 1–5, optional image, and explicit relationships where supported. Use importance 5 only for facts that must reliably shape most relevant responses. Avoid marking everything critical; that merely turns priority into decorative arithmetic.

Create relationship edges deliberately. Each edge must name two existing cards and use a concise relation label such as `member of`, `located in`, `rivals`, `owns`, or `caused`. Do not invent connections solely to make the Lore Map look busy.

## Loom Engine compiler

Use the smallest reliable mechanism:

1. style or narration rule;
2. lore-card fact;
3. Loom thread with condition and action;
4. stateful system using variables, quests, inventory, HUD, and transitions.

Keep global invariant rules in world settings or equivalent live fields. Keep entity-local behavior in its lore card. Use Loom for event-driven changes, not for static encyclopedia facts.

Every Loom thread must define a trigger, bounded condition, action, repeat behavior, and a test case. Identify precedence when multiple threads can fire together. Never claim perfect enforcement.

## Workflow

1. Identify the exact world or character package the user intends to create or update.
2. Normalize it to `references/world-schema.md`.
3. Validate JSON packages and fix only errors the user has authorized you to fix.
4. Present a compact preflight:
   - mode, title, premise, genres/tags, and content rating;
   - privacy/publication intent;
   - cover source;
   - counts by lore-card type;
   - relationship and Loom-thread counts;
   - import versus manual entry;
   - intended final action;
   - dry-run or live.
5. Open LoreWeaver in the user's browser session.
6. If signed out, ask the user to sign in themselves and say when ready.
7. Inspect the live creator and record only the controls relevant to this operation. Treat Loom `New`, `Complete setup`, settings changes, import confirmation, lore creation, and AI generation as immediate writes.
8. Prefer LoreWeaver's native import when the live UI accepts the available export/package format. Otherwise fill fields manually.
9. Before entering any story text or uploading a file, confirm the exact content being transmitted to LoreWeaver if the user has not already explicitly authorized that transmission.
10. Fill foundation fields, then lore cards, relationships, settings, and Loom threads.
11. Verify imported counts and spot-check representative cards instead of assuming an import succeeded.
12. Use a playtest link or private playtest when requested and available. Never treat a playtest as publication.
13. Default to private/draft. Do not publish, unpublish, update a public world, or change its rating/visibility without explicit direction.
14. Stop immediately before any `Complete setup`, Loom `New`, `Create entry`, `Save`, `Import`, `Update`, `Publish`, `Unpublish`, setting change, AI generation, or equivalent external write unless the user explicitly authorized that exact action in the current request.
15. At action time, confirm LoreWeaver, title, action, visibility, and transmitted content.
16. Perform the final action once, then verify the resulting title, status, counts, and URL.

For a dry run, inspect and preflight without filling fields. Filling a webpage transmits content even if nothing is saved.

## Imports, exports, and updates

- Preserve source ordering and stable card identities.
- Export or back up an existing world before broad updates when the UI permits.
- Use the creator-update diff viewer when available; report additions, modifications, removals, and visibility changes separately.
- Never replace an existing public world by creating a similarly titled duplicate.
- When a platform import is offered, inspect its mapping preview and unresolved fields before committing.
- Preserve every unmapped field under `extensions` and show conversion warnings.
- Never present the plugin's portable JSON as a native LoreWeaver export. Probe and verify one authentic export first.
- Stop if titles collide, card types are silently changed, relationships cannot be resolved, or counts differ.

## Images

Accept user-provided images for covers and lore cards. Verify each file and destination before upload. Preserve originals when resizing or cropping. Use image generation only when the user asks for generated art, and confirm separately before transmitting it to LoreWeaver.

## Consistency checks

Before browser work, check:

- unique lore-card titles or stable IDs;
- relationship endpoints exist;
- importance values are integers 1–5;
- opening state agrees with premise and character cards;
- world rules do not contradict Loom actions;
- character experiences define the featured character and user relationship;
- regular worlds have character cards for named active NPCs where practical;
- Loom actions reference valid variables, cards, quests, items, or locations;
- public metadata does not reveal private notes or hidden creator instructions.

Report blocking errors separately from warnings. Do not rewrite creative content to silence a warning without permission.

## Privacy and safety

- Worlds and stories are private by default according to LoreWeaver's public FAQ; still verify the live setting.
- Publishing exposes world settings and lore, but session story text is not intended to be shared. Never rely on this distinction without checking the live publish summary.
- Do not upload unrelated conversation history, credentials, personal data, or hidden instructions.
- Do not alter attribution, ownership, content rating, monetization, remix/download permissions, or visibility by inference.
- If a CAPTCHA appears, ask the user before attempting it.
- Before public publication, check the current LoreWeaver Community Guidelines, accurate content rating, cover-image rules, ownership/permission, and public metadata.
- If submission fails, preserve the draft where possible and report the visible error without repeated submissions.

## Suggested invocation

`Turn the finished world in this chat into a validated LoreWeaver draft.`
