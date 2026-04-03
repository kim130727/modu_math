from __future__ import annotations

from modu_math.core.base_problem import BaseProblemBuilder
from modu_math.registry.problem_registry import register_builder


@register_builder("measure_length_with_ruler")
class MeasureLengthWithRulerBuilder(BaseProblemBuilder):
    problem_type = "measure_length_with_ruler"

    def build_domain(self, raw_problem: dict) -> dict:
        m = raw_problem["measurement"]
        expected_mm = round((float(m["right_cm"]) - float(m["left_cm"])) * 10)
        return {
            "ruler": raw_problem["ruler"],
            "measurement": m,
            "expected_mm": expected_mm,
        }

    def build_render(self, raw_problem: dict, domain: dict) -> dict:
        # Reuses layout close to existing 0002.
        return {
            "canvas": {"width": 1280, "height": 720, "background": "#F7F7F7"},
            "groups": [{"id": "header"}, {"id": "ruler_group"}, {"id": "answer_group"}],
            "elements": [
                {
                    "id": "instruction",
                    "type": "text",
                    "text": raw_problem["instruction"],
                    "x": 72,
                    "y": 80,
                    "anchor": "start",
                    "font_family": "Malgun Gothic",
                    "font_size": 42,
                    "fill": "#000000",
                    "group": "header",
                    "semantic_role": "instruction",
                },
                {
                    "id": "sub_instruction",
                    "type": "text",
                    "text": raw_problem["sub_instruction"],
                    "x": 72,
                    "y": 128,
                    "anchor": "start",
                    "font_family": "Malgun Gothic",
                    "font_size": 30,
                    "fill": "#000000",
                    "group": "header",
                    "semantic_role": "sub_instruction",
                },
                {
                    "id": "ruler_body",
                    "type": "rect",
                    "x": 220,
                    "y": 330,
                    "width": 820,
                    "height": 170,
                    "stroke": "#C9A000",
                    "stroke_width": 6,
                    "fill": "none",
                    "group": "ruler_group",
                    "semantic_role": "scale",
                    "figure_type": "ruler",
                },
                {
                    "id": "answer_blank",
                    "type": "rect",
                    "x": 530,
                    "y": 615,
                    "width": 280,
                    "height": 48,
                    "stroke": "#000000",
                    "stroke_width": 2,
                    "fill": "none",
                    "group": "answer_group",
                    "semantic_role": "answer_blank",
                    "figure_type": "blank_box",
                },
            ],
        }

    def build_answer(self, raw_problem: dict, domain: dict) -> dict:
        value = str(raw_problem.get("answer_mm", domain["expected_mm"]))
        return {
            "blanks": [{"id": "answer_blank", "kind": "numeric", "value": value, "unit": "mm"}],
            "choices": raw_problem.get("choices", []),
            "answer_key": [{"target": "answer_blank", "value": value}],
        }
