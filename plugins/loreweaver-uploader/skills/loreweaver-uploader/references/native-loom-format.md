# Verified LoreWeaver Loom JSON

Verified from an authentic export supplied on July 6, 2026.

```json
{
  "version": "1.0",
  "threads": [
    {
      "sourceId": "UUID",
      "name": "Thread name",
      "description": "Purpose",
      "enabled": true,
      "conditions": [],
      "conditionLogic": "AND",
      "actions": [],
      "priority": 5,
      "sortOrder": 0,
      "tags": [],
      "color": "#8B5CF6",
      "fireOnce": false,
      "isHidden": false,
      "maxFires": null,
      "cooldownActions": null
    }
  ]
}
```

Observed condition types include `is_first_message`, `msg_keyword_any`, and `counter_lte`.

Observed action types include `set_counter`, `decrement_counter`, `show_meter`, `inject_narrative`, and `show_narrator_note`.

The converters preserve unknown condition/action objects without flattening their fields. This matters because LoreWeaver supports many more types than one sample can demonstrate.

Use:

```text
import_native_loom.py loom.json world.json --title "World title"
import_native_loom.py loom.json updated-world.json --base existing-world.json
export_native_loom.py world.json loom.json
```

When the source lacks an existing `source_id`, native export generates a stable UUID from the portable thread ID.
