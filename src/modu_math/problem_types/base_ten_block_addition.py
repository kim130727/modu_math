from __future__ import annotations

from modu_math.core.base_problem import BaseProblemBuilder
from modu_math.registry.problem_registry import register_builder


def _split_place_value(n: int) -> dict[str, int]:
    return {
        "hundreds": n // 100,
        "tens": (n % 100) // 10,
        "ones": n % 10,
    }


@register_builder("base_ten_block_addition")
class BaseTenBlockAdditionBuilder(BaseProblemBuilder):
    problem_type = "base_ten_block_addition"

    def build_domain(self, raw_problem: dict) -> dict:
        a, b = int(raw_problem["addends"][0]), int(raw_problem["addends"][1])
        return {
            "addends": [a, b],
            "decomposed": {
                "a": _split_place_value(a),
                "b": _split_place_value(b),
            },
            "sum": a + b,
        }

    def build_render(self, raw_problem: dict, domain: dict) -> dict:
        eq = f'{domain["addends"][0]}+{domain["addends"][1]}='
        return {
            "canvas": {"width": 1280, "height": 720, "background": "#F6F6F6"},
            "groups": [{"id": "header"}, {"id": "model"}, {"id": "equation"}],
            "elements": [
                {
                    "id": "instruction",
                    "type": "text",
                    "text": raw_problem["instruction"],
                    "x": 132,
                    "y": 72,
                    "anchor": "start",
                    "font_family": "Malgun Gothic",
                    "font_size": 50,
                    "fill": "#222222",
                    "group": "header",
                    "semantic_role": "instruction",
                },
                {
                    "id": "model_box",
                    "type": "rect",
                    "x": 130,
                    "y": 165,
                    "width": 550,
                    "height": 490,
                    "stroke": "#9C9CA1",
                    "stroke_width": 3,
                    "fill": "none",
                    "group": "model",
                    "semantic_role": "container",
                    "figure_type": "box",
                },
                {
                    "id": "equation_text",
                    "type": "text",
                    "text": eq,
                    "x": 900,
                    "y": 615,
                    "anchor": "middle",
                    "font_family": "Malgun Gothic",
                    "font_size": 44,
                    "fill": "#222222",
                    "group": "equation",
                    "semantic_role": "equation",
                },
                {
                    "id": "answer_blank",
                    "type": "rect",
                    "x": 1045,
                    "y": 567,
                    "width": 155,
                    "height": 78,
                    "rx": 10,
                    "stroke": "#69BEEA",
                    "stroke_width": 4,
                    "fill": "none",
                    "group": "equation",
                    "semantic_role": "answer_blank",
                    "figure_type": "blank_box",
                },
            ],
        }

    def build_answer(self, raw_problem: dict, domain: dict) -> dict:
        value = str(raw_problem.get("answer", domain["sum"]))
        return {
            "blanks": [{"id": "answer_blank", "kind": "numeric", "value": value}],
            "choices": raw_problem.get("choices", []),
            "answer_key": [{"target": "answer_blank", "value": value}],
        }
