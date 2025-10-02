from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image


@dataclass
class CompressResult:
    source: Path
    dest: Path
    original_bytes: int
    output_bytes: int

    @property
    def saved_bytes(self) -> int:
        return max(self.original_bytes - self.output_bytes, 0)

    @property
    def saved_ratio(self) -> float:
        if self.original_bytes == 0:
            return 0.0
        return self.saved_bytes / self.original_bytes


def _infer_format(path: Path) -> Optional[str]:
    ext = path.suffix.lower().lstrip(".")
    if ext in {"jpg", "jpeg"}:
        return "JPEG"
    if ext in {"png"}:
        return "PNG"
    if ext in {"webp"}:
        return "WEBP"
    return None


def compress_image(
    src: Path,
    dest: Optional[Path] = None,
    *,
    quality: int = 85,
    optimize: bool = True,
    progressive: bool = True,
    format: Optional[str] = None,
) -> CompressResult:
    src = Path(src)
    if dest is None:
        dest = src.with_suffix(src.suffix)
    dest = Path(dest)

    fmt = format or _infer_format(dest) or _infer_format(src)
    if fmt is None:
        raise ValueError("Unsupported image format; use .jpg/.jpeg/.png/.webp or set format=")

    original_bytes = src.stat().st_size if src.exists() else 0

    with Image.open(src) as im:
        save_kwargs = {}
        if fmt == "JPEG":
            save_kwargs.update(dict(quality=quality, optimize=optimize, progressive=progressive))
            im = im.convert("RGB")
        elif fmt == "PNG":
            # Pillow PNG optimize is lossless; optionally allow quantization later
            save_kwargs.update(dict(optimize=optimize))
        elif fmt == "WEBP":
            save_kwargs.update(dict(quality=quality, method=6))

        dest.parent.mkdir(parents=True, exist_ok=True)
        im.save(dest, format=fmt, **save_kwargs)

    output_bytes = dest.stat().st_size if dest.exists() else 0
    # Avoid negative wins: if output grew, keep the smaller one
    if output_bytes > 0 and original_bytes > 0 and output_bytes > original_bytes:
        # write back original bytes
        # replace with original file content
        dest.write_bytes(src.read_bytes())
        output_bytes = original_bytes
    return CompressResult(source=src, dest=dest, original_bytes=original_bytes, output_bytes=output_bytes)
