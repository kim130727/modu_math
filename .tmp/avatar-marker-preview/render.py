from pathlib import Path
from io import BytesIO
from xml.etree import ElementTree
import resvg_py
from PIL import Image

folder = Path(__file__).parent
blank_fractions = []
for source in sorted(folder.glob("avatar-*.svg")):
    ElementTree.parse(source)
    pixels = resvg_py.svg_to_bytes(svg_path=str(source), skip_system_fonts=True)
    image = Image.open(BytesIO(pixels)).convert("RGBA")
    assert image.getpixel((0, 0))[3] == 0, source
    bounds = image.getbbox()
    assert bounds and min(bounds[:2]) > 0 and max(bounds[2:]) < 200, (source, bounds)
    blank = sum(1 for r, g, b, a in image.getdata() if a == 0 or min(r, g, b) > 245)
    blank_fractions.append(blank / 40000)
    source.with_suffix(".png").write_bytes(pixels)
(folder / "contact-sheet.png").write_bytes(resvg_py.svg_to_bytes(svg_path=str(folder / "contact-sheet.svg")))
print("22 SVGs parsed/rendered; transparent corners; no clipped silhouettes.")
print("Visually unmarked fraction:", round(min(blank_fractions), 3), "-", round(max(blank_fractions), 3))
