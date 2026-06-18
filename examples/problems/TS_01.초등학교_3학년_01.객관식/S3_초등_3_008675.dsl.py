from __future__ import annotations

from modu_math.dsl import Canvas, CircleSlot, PathSlot, ProblemTemplate, RectSlot, Region, TextSlot


YELLOW = "#d5c400"
BLACK = "#111111"
RED = "#ff0000"
MAGENTA = "#e4007f"


def _square(id_: str, *, x: float, y: float) -> RectSlot:
    return RectSlot(
        id=id_,
        prompt="",
        x=x,
        y=y,
        width=152.0,
        height=152.0,
        fill="#ffffff",
        stroke=YELLOW,
        stroke_width=2.0,
    )


def _center_dot(id_: str, *, cx: float, cy: float) -> CircleSlot:
    return CircleSlot(id=id_, prompt="", cx=cx, cy=cy, r=3.5, fill=MAGENTA, stroke="none", stroke_width=0.0)


def _base_arc(id_: str, *, cx: float, cy: float, r: float = 76.0) -> PathSlot:
    return PathSlot(
        id=id_,
        prompt="",
        d=f"M {cx + r} {cy} A {r} {r} 0 1 0 {cx} {cy + r}",
        stroke=BLACK,
        stroke_width=2.1,
    )


def _correct_completion_arc(id_: str, *, cx: float, cy: float, r: float = 76.0) -> PathSlot:
    return PathSlot(
        id=id_,
        prompt="",
        d=f"M {cx} {cy + r} A {r} {r} 0 0 0 {cx + r} {cy}",
        stroke=RED,
        stroke_width=2.1,
    )


def _corner_completion_arc(id_: str, *, cx: float, cy: float, r: float = 76.0) -> PathSlot:
    corner_cx = cx + r
    corner_cy = cy + r
    return PathSlot(
        id=id_,
        prompt="",
        d=f"M {corner_cx - r} {corner_cy} A {r} {r} 0 0 1 {corner_cx} {corner_cy - r}",
        stroke=RED,
        stroke_width=2.1,
    )


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008675",
        title="원을 바르게 완성한 것을 선택하세요.",
        canvas=Canvas(width=900.0, height=250.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.header.text",'slot.header.text.copy4', 'slot.header.text.copy4.copy5', 'slot.header.text.copy4.copy5.copy6'),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.left.square",
                    "slot.choice.left.base",
                    "slot.choice.left.center",
                    "slot.choice.middle.square",
                    "slot.choice.middle.base",
                    "slot.choice.middle.red",
                    "slot.choice.middle.center",
                    "slot.choice.right.square",
                    "slot.choice.right.base",
                    "slot.choice.right.red",
                    "slot.choice.right.center",
                ),
            ),
        ),
        slots=(TextSlot(
                id="slot.header.text",
                prompt="",
                text = '원을 바르게 완성한 것을 선택하세요.', style_role="question",
                x = 72, y = 29, font_size = 26, fill = '#111111'),
            _square("slot.choice.left.square", x=137.0, y=74.0),
            _base_arc("slot.choice.left.base", cx=213.0, cy=150.0),
            _center_dot("slot.choice.left.center", cx=213.0, cy=150.0),
            _square("slot.choice.middle.square", x=444.0, y=74.0),
            _base_arc("slot.choice.middle.base", cx=520.0, cy=150.0),
            _correct_completion_arc("slot.choice.middle.red", cx=520.0, cy=150.0),
            _center_dot("slot.choice.middle.center", cx=520.0, cy=150.0),
            _square("slot.choice.right.square", x=672.0, y=74.0),
            _base_arc("slot.choice.right.base", cx=748.0, cy=150.0),
            _corner_completion_arc("slot.choice.right.red", cx=748.0, cy=150.0),
            _center_dot("slot.choice.right.center", cx=748.0, cy=150.0),TextSlot(id = 'slot.header.text.copy4', prompt = '', text = '가.', x = 90, y = 95, font_size = 25, fill = '#111111'), TextSlot(id = 'slot.header.text.copy4.copy5', prompt = '', text = '나.', x = 345, y = 95, font_size = 25, fill = '#111111'), TextSlot(id = 'slot.header.text.copy4.copy5.copy6', prompt = '', text = '다.', x = 625, y = 95, font_size = 25, fill = '#111111')),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008675",
    "problem_type": "circle_completion_choice",
    "metadata": {
        "language": "ko",
        "question": "원을 바르게 완성한 것을 선택하세요.",
        "instruction": "정답과 해설 영역은 렌더링하지 않는다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.circle_completion_choices",
                "type": "circle_completion_choices",
                "description": "제시된 원의 빈 부분을 보기의 빨간 선으로 완성하는 시각 선택 문제",
            }
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle_completion_choices"],
                "target_ref": "answer.target",
                "condition_refs": [],
            },
            "plan": {"method": "visual_comparison", "description": "각 보기의 빨간 선이 원호와 자연스럽게 이어지는지 비교한다."},
            "execute": {"expected_operations": ["compare_shapes"]},
            "review": {"check_methods": ["curve_continuity"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_picture", "description": "원을 바르게 완성한 그림"},
        "value": "나",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008675",
    "problem_type": "circle_completion_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "원을 바르게 완성한 그림",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [{"ref": "obj.circle_completion_choices", "value": "원호 보기"}],
    "target": {"ref": "answer.target", "type": "selected_picture"},
    "method": "visual_comparison",
    "plan": ["보기의 선이 원호와 이어지는지 비교한다."],
    "steps": [{"id": "step.1", "expr": "각 보기의 빨간 선과 검은 원호의 연결 상태를 비교한다.", "value": ""}],
    "checks": [{"id": "check.1", "expr": "정답과 해설 문장이 렌더링되지 않는다.", "expected": True, "actual": True, "pass": True}],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_picture", "description": "원을 바르게 완성한 그림"},
        "value": "나",
        "unit": "",
    },
}
