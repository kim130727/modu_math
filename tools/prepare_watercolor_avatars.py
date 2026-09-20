"""Resize/re-encode generated transparent cutouts; never remove or repaint pixels.

uv run --no-project --with pillow python tools/prepare_watercolor_avatars.py SOURCE_DIR
"""
import sys
from pathlib import Path
from PIL import Image

SOURCES = {
    "pencil-boy": "exec-77bc5c9b-454c-4595-9f2c-af7329b82aa1.png",
    "waving-girl": "exec-6a946ed4-ca42-4fcc-ba63-0c0a4e0b9f70.png",
    "thinking-boy": "exec-4b56eb8e-fdf7-4e0c-b735-0bb8d4f83165.png",
    "pointing-girl": "exec-1955fba1-4384-472c-bad4-8a10977ebe63.png",
}
destination = Path(__file__).resolve().parents[1] / "src/modu_math_web/editor_next/src/assets/watercolor"
destination.mkdir(parents=True, exist_ok=True)
for name, filename in SOURCES.items():
    with Image.open(Path(sys.argv[1]) / filename) as image:
        assert image.mode == "RGBA" and image.getchannel("A").getextrema()[0] == 0
        image.thumbnail((512, 768), Image.Resampling.LANCZOS)
        target = destination / f"{name}.webp"
        image.save(target, "WEBP", quality=88, method=6)
        with Image.open(target) as encoded:
            assert encoded.mode == "RGBA"
            assert encoded.getpixel((0, 0))[3] == 0
        print(f"{name}: {image.width}x{image.height}, {target.stat().st_size} bytes")
