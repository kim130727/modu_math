"""Image-first pipeline helpers: images -> semantic -> svg + match-ready metadata."""

from __future__ import annotations

import base64
import hashlib
from io import BytesIO
import struct
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from math_problem_pipeline.models.semantic_models import UnknownVisualMathProblem

SUPPORTED_IMAGE_EXTS = {".png", ".bmp"}


def list_supported_images(images_dir: Path) -> list[Path]:
    if not images_dir.exists():
        return []
    return sorted(
        p
        for p in images_dir.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_IMAGE_EXTS
    )


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_image_size(path: Path) -> tuple[int | None, int | None]:
    ext = path.suffix.lower()
    if ext == ".png":
        return _png_size(path)
    if ext == ".bmp":
        return _bmp_size(path)
    return None, None


def detect_image_meta(path: Path) -> tuple[int | None, int | None, str]:
    """Detect width/height/format from bytes, independent of file extension."""
    try:
        with Image.open(path) as im:
            w, h = im.size
            fmt = (im.format or path.suffix.lower().lstrip(".") or "unknown").lower()
            return int(w), int(h), fmt
    except (UnidentifiedImageError, OSError):
        w, h = probe_image_size(path)
        fmt = path.suffix.lower().lstrip(".") or "unknown"
        return w, h, fmt


def build_image_semantic(
    image_path: Path,
    problem_id: str,
    source_path: str,
    relative_image_href: str,
) -> UnknownVisualMathProblem:
    w, h, fmt = detect_image_meta(image_path)
    digest = sha256_file(image_path)
    data_uri = image_data_uri(image_path)

    return UnknownVisualMathProblem(
        problem_id=problem_id,
        source_path=source_path,
        page_number=1,
        type="unknown_visual_math_problem",
        question_text=f"Image problem: {image_path.stem}",
        type_guess="unknown_visual_math_problem",
        type_guess_reason="image_input_pipeline",
        confidence=0.95,
        coordinates={
            "source_coordinates": {
                "image_path": relative_image_href,
                "image_format": fmt,
                "image_width": w,
                "image_height": h,
                "sha256": digest,
                "file_size": image_path.stat().st_size,
                "image_data_uri": data_uri,
            },
            "semantic_coordinates": {},
            "render_coordinates": {},
        },
    )


def _png_size(path: Path) -> tuple[int | None, int | None]:
    with path.open("rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return None, None
    w = struct.unpack(">I", header[16:20])[0]
    h = struct.unpack(">I", header[20:24])[0]
    return int(w), int(h)


def _bmp_size(path: Path) -> tuple[int | None, int | None]:
    with path.open("rb") as f:
        header = f.read(26)
    if len(header) < 26 or header[:2] != b"BM":
        return None, None
    w = struct.unpack("<i", header[18:22])[0]
    h = struct.unpack("<i", header[22:26])[0]
    return abs(int(w)), abs(int(h))


def _guess_mime_from_bytes(raw: bytes, ext: str) -> str:
    if raw.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if raw.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if raw.startswith(b"BM"):
        return "image/bmp"
    return {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "bmp": "image/bmp",
    }.get(ext, f"image/{ext or 'octet-stream'}")


def image_data_uri(path: Path) -> str:
    """Return a robust data URI for SVG embedding.

    All images are normalized to PNG bytes when decodable. This avoids
    extension/content mismatches and improves SVG renderer compatibility.
    """
    try:
        with Image.open(path) as im:
            buf = BytesIO()
            im.convert("RGBA").save(buf, format="PNG")
            raw = buf.getvalue()
        mime = "image/png"
    except (UnidentifiedImageError, OSError):
        raw = path.read_bytes()
        ext = path.suffix.lower().lstrip(".")
        mime = _guess_mime_from_bytes(raw, ext)

    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{b64}"
