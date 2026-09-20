"""WebP re-encoding only; registration and compositing happen in the editor."""
from pathlib import Path
import sys
from PIL import Image

root = Path(__file__).resolve().parents[1]
destination = root / "src/modu_math_web/editor_next/src/assets/watercolor"
sources = {
    "heads": "exec-4e5873a2-d036-444d-999a-b464dc476383.png",
    "bodies": "exec-acb144e5-e9b3-489b-9faa-b4fbc6a3726b.png",
    "heads-v2": "exec-dced7ac9-513a-448d-a59d-1d0b52fa1f52.png",
}
for name, filename in sources.items():
    with Image.open(Path(sys.argv[1]) / filename) as image:
        assert image.mode == "RGBA"
        image.save(destination / f"{name}.webp", "WEBP", quality=92, method=6)
        print(name, image.size, (destination / f"{name}.webp").stat().st_size)
