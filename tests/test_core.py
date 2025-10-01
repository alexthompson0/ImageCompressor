from pathlib import Path

import pytest

from compressor.core import _infer_format


@pytest.mark.parametrize("name,fmt", [
    ("x.jpg", "JPEG"),
    ("x.jpeg", "JPEG"),
    ("x.png", "PNG"),
    ("x.webp", "WEBP"),
    ("x.txt", None),
])
def test_infer_format(name, fmt):
    assert _infer_format(Path(name)) == fmt

