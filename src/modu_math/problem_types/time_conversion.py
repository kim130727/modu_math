from __future__ import annotations

from modu_math.core.base_problem import BaseProblemBuilder
from modu_math.registry.problem_registry import register_builder


@register_builder("time_conversion_fill_blank")
@register_builder("fill_in_blank")
class TimeConversionBuilder(BaseProblemBuilder):
    problem_type = "time_conversion_fill_blank"

    def build_domain(self, raw_problem: dict) -> dict:
        q = raw_problem["question"]
        answer = int(q["left_seconds"]) - int(q["minutes"]) * 60
        return {
            "left_seconds": int(q["left_seconds"]),
            "minutes": int(q["minutes"]),
            "unit_from": q["unit_from"],
            "unit_mid": q["unit_mid"],
            "unit_to": q["unit_to"],
            "blank_symbol": q.get("blank_symbol", "□"),
            "computed_answer": answer,
        }

    def build_render(self, raw_problem: dict, domain: dict) -> dict:
        expr = (
            f'{domain["left_seconds"]}{domain["unit_from"]}='
            f'{domain["minutes"]}{domain["unit_mid"]} '
            f'{domain["blank_symbol"]}{domain["unit_to"]}'
        )
        return {
            "canvas": {"width": 1280, "height": 720, "background": "#F6F6F6"},
            "groups": [{"id": "question"}, {"id": "answer"}],
            "elements": [
                {
                    "id": "instruction",
                    "type": "text",
                    "text": raw_problem["instruction"],
                    "x": 72,
                    "y": 92,
                    "anchor": "start",
                    "font_family": "Malgun Gothic",
                    "font_size": 42,
                    "fill": "#000000",
                    "group": "question",
                    "semantic_role": "instruction",
                },
                {
                    "id": "question_box",
                    "type": "rect",
                    "x": 280,
                    "y": 240,
                    "width": 720,
                    "height": 180,
                    "rx": 24,
                    "stroke": "#000000",
                    "stroke_width": 3,
                    "fill": "none",
                    "group": "question",
                    "semantic_role": "question_container",
                    "figure_type": "rounded_box",
                },
                {
                    "id": "equation",
                    "type": "text",
                    "text": expr,
                    "x": 640,
                    "y": 345,
                    "anchor": "middle",
                    "font_family": "Malgun Gothic",
                    "font_size": 54,
                    "fill": "#000000",
                    "group": "question",
                    "semantic_role": "equation",
                },
                {
                    "id": "answer_blank",
                    "type": "rect",
                    "x": 818,
                    "y": 526,
                    "width": 122,
                    "height": 50,
                    "rx": 8,
                    "stroke": "#000000",
                    "stroke_width": 2,
                    "fill": "none",
                    "group": "answer",
                    "semantic_role": "answer_blank",
                    "figure_type": "blank_box",
                },
            ],
        }

    def build_answer(self, raw_problem: dict, domain: dict) -> dict:
        value = str(raw_problem.get("answer", domain["computed_answer"]))
        return {
            "blanks": [{"id": "answer_blank", "kind": "numeric", "value": value, "unit": domain["unit_to"]}],
            "choices": raw_problem.get("choices", []),
            "answer_key": [{"target": "answer_blank", "value": value}],
        }
