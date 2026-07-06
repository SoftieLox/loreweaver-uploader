# Contributing

Thanks for helping improve LoreWeaver Uploader.

## Before opening a change

1. Keep authentic user exports private.
2. Create synthetic fixtures that preserve structure without preserving prose.
3. Preserve unknown native LoreWeaver fields during conversion.
4. Never weaken confirmation requirements around creation, deletion, imports, generation, or publication.
5. Run:

```text
python scripts/validate_release.py
```

## Pull requests

Explain:

- the behavior changed;
- the LoreWeaver surface or export format involved;
- how privacy and write safety are preserved;
- the tests added or updated.

Avoid committing credentials, browser state, exports containing personal lore, generated caches, or operational logs.
