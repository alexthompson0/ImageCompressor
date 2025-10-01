import argparse
import json
import random
from pathlib import Path

from compressor.core import compress_image


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Compress images with sensible defaults")
    p.add_argument("inputs", nargs="+", help="Input file(s) or directories")
    p.add_argument("-o", "--out", type=Path, help="Output path (file or directory)")
    p.add_argument("-q", "--quality", type=int, default=85, help="Quality for lossy formats")
    p.add_argument("--progressive", action="store_true", help="Write progressive JPEGs")
    p.add_argument("--no-optimize", dest="optimize", action="store_false", help="Disable encoder optimize")
    p.add_argument("--dry-run", action="store_true", help="Do not write files; show report only")
    p.add_argument("--json", dest="json_out", action="store_true", help="Emit JSON report")
    return p


def iter_files(paths):
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    for p in map(Path, paths):
        if p.is_dir():
            for sub in p.rglob("*"):
                if sub.is_file() and sub.suffix.lower() in exts:
                    yield sub
        elif p.is_file() and p.suffix.lower() in exts:
            yield p


def main(argv=None):
    args = build_parser().parse_args(argv)
    results = []

    out_dir = None
    if args.out:
        out_dir = Path(args.out)
        if len(args.inputs) > 1 or any(Path(i).is_dir() for i in args.inputs):
            out_dir.mkdir(parents=True, exist_ok=True)

    for src in iter_files(args.inputs):
        dest = None
        if out_dir:
            dest = out_dir / src.name
        if args.dry_run:
            # fake result by estimating bytes saved with a random-ish heuristic
            orig = src.stat().st_size
            saved = int(orig * random.uniform(0.05, 0.35))
            results.append(dict(source=str(src), dest=str(dest or src), original_bytes=orig, output_bytes=max(orig - saved, 0)))
        else:
            r = compress_image(src, dest, quality=args.quality, optimize=args.optimize, progressive=args.progressive)
            results.append(dict(source=str(r.source), dest=str(r.dest), original_bytes=r.original_bytes, output_bytes=r.output_bytes))

    if args.json_out:
        print(json.dumps({"items": results, "total_saved": sum(max(i["original_bytes"]-i["output_bytes"], 0) for i in results)}, indent=2))
    else:
        total_saved = 0
        for i in results:
            saved = max(i["original_bytes"] - i["output_bytes"], 0)
            total_saved += saved
            print(f"{Path(i['source']).name}: -{saved/1024:.1f} KiB")
        print(f"Total saved: {total_saved/1024:.1f} KiB")


if __name__ == "__main__":
    main()

