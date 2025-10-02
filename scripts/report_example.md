# Compression Report Idea

Example of what a JSON report might look like and how it can be consumed in a CI step (not wired up yet).

```json
{
  "items": [
    {"source": "foo.jpg", "dest": "out/foo.jpg", "original_bytes": 120034, "output_bytes": 84012}
  ],
  "total_saved": 36022
}
```

Future: add a small HTML renderer to visualize savings per-file.

