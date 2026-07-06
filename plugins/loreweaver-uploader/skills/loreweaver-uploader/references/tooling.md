# Tooling quick reference

All scripts use Python's standard library.

```text
validate_world.py world.json
qa_report.py world.json
analyze_lore.py world.json
estimate_context.py world.json
build_playtest_plan.py world.json
diff_world.py current.json proposed.json
version_history.py snapshot world.json history/
version_history.py list history/
version_history.py restore history/snapshot.json restored.json
convert_fictionlab.py fictionlab.json world.json
convert_character_card.py character.json world.json
convert_lorebook.py lorebook.json world.json
import_native_lore.py lore-export.json world.json --title "World title"
export_native_lore.py world.json lore-export.json
import_native_loom.py loom.json world.json --title "World title"
import_native_loom.py loom.json updated.json --base existing.json
export_native_loom.py world.json loom.json
prepare_public_copy.py private.json review-copy.json
verify_import.py expected.json observed.json
probe_export.py authentic-export.json
check_ui_contract.py expected.json observed.json
record_ui_contract.py observed.json current.json history/
run_fixture_tests.py
```

The portable package is a review and automation format. Only `export_native_lore.py` produces the verified LoreWeaver native lore-array shape; it is not a full-world export.

Converters never upload, publish, or change visibility. The publication-copy tool removes private cards and metadata but deliberately leaves the result private for human review.
