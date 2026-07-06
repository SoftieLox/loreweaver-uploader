# LoreWeaver Uploader

[![Validate marketplace](https://github.com/SoftieLox/loreweaver-uploader/actions/workflows/validate.yml/badge.svg)](https://github.com/SoftieLox/loreweaver-uploader/actions/workflows/validate.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-violet.svg)](LICENSE)

A Codex plugin by SoftieLox for designing, validating, converting, playtesting, and publishing LoreWeaver AI worlds and character experiences.

## Highlights

- Verified native LoreWeaver lore and Loom JSON round-tripping
- World, character, lore-card, relationship, and Loom Engine authoring
- FictionLab, Character Card, SillyTavern, and generic lorebook conversion
- Validation, canon analysis, context estimation, QA, diffs, snapshots, and playtest plans
- Privacy-safe publication preparation
- Authenticated browser workflows with explicit confirmation before external writes

## Install

Add the public marketplace:

```text
codex plugin marketplace add softielox/loreweaver-uploader
```

Then install the plugin:

```text
codex plugin add loreweaver-uploader@softielox
```

Restart Codex and begin a new thread after installation.

## Validation coverage

Automated checks run on Windows and Linux with Python 3.11 and 3.12. They verify marketplace structure, manifest metadata, bundled assets, skill packaging, prohibited generated files, converters, validators, native Lore and Loom round-trips, diffs, QA, import reconciliation, privacy-copy preparation, and synthetic regression fixtures.

Live LoreWeaver creation, deletion, publication, full-world exports, non-null native image values, and condition/action types absent from supplied exports still require targeted manual verification.

## Safety

The plugin defaults to private drafts, never handles passwords or browser tokens, and requires confirmation before imports, saves, generation, deletion, or publication.

## Author

SoftieLox
