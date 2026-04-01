"""Sample semantic JSON fixtures for bootstrapping."""

from __future__ import annotations

from pathlib import Path

from math_problem_pipeline.utils.io import ensure_dir, write_json


SAMPLES: list[tuple[str, dict]] = [
    (
        "sample_p0001_q0001.semantic.json",
        {
            "schema_version": "0.1.0",
            "problem_id": "sample_p0001_q0001",
            "source_pdf": "sample_book.pdf",
            "page_number": 1,
            "type": "multiple_choice_text",
            "question_text": "다음 중 8의 약수는 무엇인가요?",
            "choices": ["3", "4", "5", "7"],
            "answer": "4",
            "bbox": {"x0": 50, "y0": 80, "x1": 500, "y1": 220},
            "confidence": 0.93,
            "warnings": [],
            "render_hint": {"alignment": "left"},
            "coordinates": {
                "source_coordinates": {"page_width": 595, "page_height": 842},
                "semantic_coordinates": {},
                "render_coordinates": {},
            },
        },
    ),
    (
        "sample_p0001_q0002.semantic.json",
        {
            "schema_version": "0.1.0",
            "problem_id": "sample_p0001_q0002",
            "source_pdf": "sample_book.pdf",
            "page_number": 1,
            "type": "arithmetic_expression",
            "question_text": "식을 계산하세요.",
            "expression": "(18 + 6) / 3 - 4",
            "answer": "4",
            "bbox": {"x0": 50, "y0": 240, "x1": 500, "y1": 330},
            "confidence": 0.95,
            "warnings": [],
            "render_hint": {"alignment": "left"},
            "coordinates": {
                "source_coordinates": {"page_width": 595, "page_height": 842},
                "semantic_coordinates": {},
                "render_coordinates": {},
            },
        },
    ),
    (
        "sample_p0001_q0003.semantic.json",
        {
            "schema_version": "0.1.0",
            "problem_id": "sample_p0001_q0003",
            "source_pdf": "sample_book.pdf",
            "page_number": 1,
            "type": "fraction_shaded_area",
            "question_text": "8칸 중 3칸이 색칠된 분수를 구하세요.",
            "fraction": {
                "shape": "rectangle",
                "total_parts": 8,
                "shaded_parts": 3,
                "rows": 2,
                "cols": 4,
                "partition": "grid",
                "shaded_indices": [0, 1, 2],
            },
            "answer": "3/8",
            "bbox": {"x0": 50, "y0": 340, "x1": 500, "y1": 480},
            "confidence": 0.9,
            "warnings": [],
            "render_hint": {"alignment": "left"},
            "coordinates": {
                "source_coordinates": {"page_width": 595, "page_height": 842},
                "semantic_coordinates": {"grid_origin": [0, 0]},
                "render_coordinates": {},
            },
        },
    ),
    (
        "sample_p0001_q0004.semantic.json",
        {
            "schema_version": "0.1.0",
            "problem_id": "sample_p0001_q0004",
            "source_pdf": "sample_book.pdf",
            "page_number": 1,
            "type": "clock_reading",
            "question_text": "시계가 가리키는 시각을 쓰세요.",
            "clock": {"hour": 3, "minute": 30, "hour_angle": None, "minute_angle": None},
            "answer": "3시 30분",
            "bbox": {"x0": 50, "y0": 490, "x1": 500, "y1": 620},
            "confidence": 0.92,
            "warnings": ["clock_hand_angle_inferred"],
            "render_hint": {"alignment": "left"},
            "coordinates": {
                "source_coordinates": {"page_width": 595, "page_height": 842},
                "semantic_coordinates": {"clock_center": [0.5, 0.5]},
                "render_coordinates": {},
            },
        },
    ),
    (
        "sample_p0002_q0001.semantic.json",
        {
            "schema_version": "0.1.0",
            "problem_id": "sample_p0002_q0001",
            "source_pdf": "sample_book.pdf",
            "page_number": 2,
            "type": "geometry_basic",
            "question_text": "삼각형 ABC에서 변 AB의 길이가 5일 때 둘레를 구하세요.",
            "points": [
                {"label": "A", "x": 0.0, "y": 0.0},
                {"label": "B", "x": 3.0, "y": 0.0},
                {"label": "C", "x": 1.5, "y": 2.2},
            ],
            "segments": [
                {"start": "A", "end": "B", "length_label": "5"},
                {"start": "B", "end": "C", "length_label": "4"},
                {"start": "C", "end": "A", "length_label": "4"},
            ],
            "angles": [],
            "polygons": [["A", "B", "C"]],
            "answer": "13",
            "bbox": {"x0": 60, "y0": 90, "x1": 520, "y1": 280},
            "confidence": 0.89,
            "warnings": [],
            "render_hint": {"alignment": "left"},
            "coordinates": {
                "source_coordinates": {"page_width": 595, "page_height": 842},
                "semantic_coordinates": {
                    "vertices": {"A": [0, 0], "B": [3, 0], "C": [1.5, 2.2]}
                },
                "render_coordinates": {},
            },
        },
    ),
    (
        "sample_p0002_q0002.semantic.json",
        {
            "schema_version": "0.1.0",
            "problem_id": "sample_p0002_q0002",
            "source_pdf": "sample_book.pdf",
            "page_number": 2,
            "type": "table_or_chart_basic",
            "question_text": "다음 표를 보고 사과가 바나나보다 몇 개 더 많은지 구하세요.",
            "table": {
                "headers": ["과일", "개수"],
                "rows": [["사과", "12"], ["바나나", "9"], ["포도", "7"]],
            },
            "chart": None,
            "answer": "3",
            "bbox": {"x0": 60, "y0": 300, "x1": 520, "y1": 520},
            "confidence": 0.88,
            "warnings": [],
            "render_hint": {"alignment": "left"},
            "coordinates": {
                "source_coordinates": {"page_width": 595, "page_height": 842},
                "semantic_coordinates": {
                    "table_cells": {"rows": 4, "cols": 2}
                },
                "render_coordinates": {},
            },
        },
    ),
]


def write_sample_semantics(output_dir: Path) -> None:
    ensure_dir(output_dir)
    for name, payload in SAMPLES:
        write_json(output_dir / name, payload)
