import base64
from pathlib import Path
import resvg_py

root = Path(__file__).resolve().parents[1]
assets = root / "src/modu_math_web/editor_next/src/assets/watercolor"
cells = []
for index, name in enumerate(["pencil-boy", "waving-girl", "thinking-boy", "pointing-girl"]):
    data = base64.b64encode((assets / f"{name}.webp").read_bytes()).decode()
    x = index * 256
    cells.append(f'<rect x="{x}" width="256" height="384" fill="{["#fffdf7", "#e8f0fd"][index % 2]}"/><image x="{x}" width="256" height="384" href="data:image/webp;base64,{data}"/>')
svg = '<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="384">' + "".join(cells) + '</svg>'
(root / ".tmp/watercolor-assets-preview.png").write_bytes(resvg_py.svg_to_bytes(svg_string=svg))
