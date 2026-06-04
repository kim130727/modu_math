from __future__ import annotations

import json
import re
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .llm_adapter import VisionAnalysis


@dataclass(frozen=True)
class ProblemClassification:
    problem_id: str
    problem_type: str
    template_id: str
    detected_objects: tuple[str, ...]
    text_lines: tuple[str, ...]
    template_hints: tuple[str, ...]
    canvas_width: int
    canvas_height: int
    confidence: float
    notes: tuple[str, ...]


class VisionAdapter(Protocol):
    def analyze_png(
        self,
        *,
        image_path: Path,
        problem_id: str,
        ocr_lines: tuple[str, ...] = (),
    ) -> VisionAnalysis: ...


def classify_png_problem(
    *,
    image_path: Path,
    problem_id: str,
    ocr_lines: tuple[str, ...] = (),
    llm_adapter: VisionAdapter | None = None,
) -> ProblemClassification:
    canvas_width, canvas_height = _read_png_size(image_path)
    sidecar = _load_sidecar_layout_text(image_path)

    llm_signal: VisionAnalysis | None = None
    if llm_adapter is not None:
        try:
            llm_signal = llm_adapter.analyze_png(image_path=image_path, problem_id=problem_id, ocr_lines=ocr_lines)
        except Exception:
            llm_signal = None

    text_lines = _merge_text_lines(
        preferred=ocr_lines,
        llm_lines=llm_signal.text_lines if llm_signal else (),
        sidecar_lines=sidecar,
    )
    detected_objects = _merge_object_signals(text_lines=text_lines, llm_signal=llm_signal)
    template_hints = _merge_hints(text_lines=text_lines, llm_signal=llm_signal)

    has_choice = _looks_like_multiple_choice(text_lines)
    has_two_panel = any("(1)" in line for line in text_lines) and any("(2)" in line for line in text_lines)
    has_blank = any(token in line for token in ("□", "빈칸", "?", "▢") for line in text_lines)

    template_id = _pick_template_id(detected_objects=detected_objects, has_choice=has_choice, has_two_panel=has_two_panel)
    problem_type = _pick_problem_type(detected_objects=detected_objects, has_choice=has_choice, has_blank=has_blank)
    confidence = _estimate_confidence(llm_signal=llm_signal, has_choice=has_choice, detected_objects=detected_objects)

    notes: list[str] = []
    if llm_signal is None:
        notes.append("classification_without_llm")
    if not text_lines:
        notes.append("no_text_detected")
    if has_two_panel:
        notes.append("detected_two_panel_structure")
    if has_choice:
        notes.append("detected_choice_structure")

    if llm_signal is not None:
        notes.extend(llm_signal.notes)

    return ProblemClassification(
        problem_id=problem_id,
        problem_type=problem_type,
        template_id=template_id,
        detected_objects=detected_objects,
        text_lines=text_lines,
        template_hints=template_hints,
        canvas_width=canvas_width,
        canvas_height=canvas_height,
        confidence=confidence,
        notes=tuple(_dedup(notes)),
    )


def _read_png_size(image_path: Path) -> tuple[int, int]:
    # PNG IHDR stores width/height at bytes 16:24.
    data = image_path.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return (800, 600)
    width, height = struct.unpack(">II", data[16:24])
    return (int(width), int(height))


def _load_sidecar_layout_text(image_path: Path) -> tuple[str, ...]:
    layout_path = image_path.with_suffix(".layout.json")
    if not layout_path.exists():
        return ()
    try:
        payload = json.loads(layout_path.read_text(encoding="utf-8"))
    except Exception:
        return ()

    nodes = payload.get("nodes")
    if not isinstance(nodes, list):
        return ()
    out: list[str] = []
    for node in nodes:
        if not isinstance(node, dict):
            continue
        if node.get("type") != "text":
            continue
        props = node.get("properties")
        if not isinstance(props, dict):
            continue
        text = props.get("text")
        if not isinstance(text, str):
            continue
        stripped = text.strip()
        if stripped:
            out.append(stripped)
    return tuple(_dedup(out))


def _merge_text_lines(
    *,
    preferred: tuple[str, ...],
    llm_lines: tuple[str, ...],
    sidecar_lines: tuple[str, ...],
) -> tuple[str, ...]:
    if preferred:
        return tuple(_dedup(preferred))
    if llm_lines:
        return tuple(_dedup(llm_lines))
    return tuple(_dedup(sidecar_lines))


def _merge_object_signals(*, text_lines: tuple[str, ...], llm_signal: VisionAnalysis | None) -> tuple[str, ...]:
    detected: list[str] = list(llm_signal.detected_objects) if llm_signal else []
    text_blob = " ".join(text_lines).lower()
    keyword_map = {
        "cube": ("정육면체", "직육면체", "cube"),
        "triangle": ("삼각형", "triangle"),
        "circle": ("원", "원의", "circle"),
        "grid": ("격자", "칸", "grid", "행", "열"),
        "fraction_area_model": ("분수", "/", "fraction"),
        "arrow": ("화살표", "→", "←", "arrow"),
        "label_slot": ("점", "꼭짓점", "label"),
    }
    for object_name, words in keyword_map.items():
        if any(word in text_blob for word in words):
            detected.append(object_name)
    if detected:
        detected.append("diagram_template")
    return tuple(_dedup(detected))


def _merge_hints(*, text_lines: tuple[str, ...], llm_signal: VisionAnalysis | None) -> tuple[str, ...]:
    hints: list[str] = list(llm_signal.template_hints) if llm_signal else []
    text_blob = " ".join(text_lines)
    if _looks_like_multiple_choice(text_lines):
        hints.append("multiple_choice")
    if any(token in text_blob for token in ("(", ")", "(1)", "(2)")):
        hints.append("enumerated_steps")
    if any(token in text_blob for token in ("□", "빈칸", "?", "▢")):
        hints.append("blank_answer")
    return tuple(_dedup(hints))


def _looks_like_multiple_choice(lines: tuple[str, ...]) -> bool:
    if any(re.search(r"[①②③④⑤]", line) for line in lines):
        return True
    return sum(1 for line in lines if re.match(r"^\s*\d+\.", line)) >= 3


def _pick_template_id(*, detected_objects: tuple[str, ...], has_choice: bool, has_two_panel: bool) -> str:
    priority = (
        ("fraction_area_model", "fraction_area_model"),
        ("cube", "cube_diagram_label"),
        ("triangle", "triangle_diagram_label"),
        ("circle", "circle_diagram_label"),
        ("grid", "grid_diagram"),
        ("arrow", "arrow_flow"),
    )
    for object_name, template_id in priority:
        if object_name in detected_objects:
            return template_id
    if has_choice:
        return "multiple_choice"
    if has_two_panel:
        return "arithmetic_two_panel"
    return "generic_text_blank"


def _pick_problem_type(*, detected_objects: tuple[str, ...], has_choice: bool, has_blank: bool) -> str:
    if "fraction_area_model" in detected_objects:
        return "fraction_area_model"
    if "cube" in detected_objects:
        return "solid_geometry_cube"
    if "triangle" in detected_objects:
        return "triangle_geometry"
    if "circle" in detected_objects:
        return "circle_geometry"
    if has_choice:
        return "multiple_choice"
    if has_blank:
        return "fill_in_blank"
    return "arithmetic_word_problem"


def _estimate_confidence(
    *,
    llm_signal: VisionAnalysis | None,
    has_choice: bool,
    detected_objects: tuple[str, ...],
) -> float:
    base = 0.55
    if llm_signal is not None:
        base += 0.2
    if has_choice:
        base += 0.1
    if detected_objects:
        base += 0.1
    return min(0.95, base)


def _dedup(values: list[str] | tuple[str, ...]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        stripped = value.strip()
        if not stripped or stripped in seen:
            continue
        seen.add(stripped)
        out.append(stripped)
    return out

