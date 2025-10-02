# Dev notes

- Consider adding a --target-size option to approach a desired KB size
- Add a small heuristic to avoid making files larger (e.g., PNG to JPEG guard)
- Add a summary table for folder runs
- Explore lossy PNG (quantization) via pillow-simd or external tools

Bench ideas (manual, not automated):
- Try a sample set of mixed JPG/PNG icons and photos
- Compare qualities 70/80/90 for visual delta

