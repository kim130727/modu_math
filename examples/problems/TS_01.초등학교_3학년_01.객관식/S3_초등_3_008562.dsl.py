from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008562",
        title="계산 결과가 더 큰 것을 찾아 기호를 선택하세요.",
        canvas=Canvas(width=670, height=400, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qnum", "slot.qtext"),
            ),
            Region(
                id="region.choices",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.choice_box", "slot.opt1", "slot.opt2"),
            ),
            Region(
                id="region.work",
                role="supporting",
                flow="absolute",
                slot_ids=("slot.work1", "slot.work2", "slot.compare"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="27.",
                style_role="question",
                x=24.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="계산 결과가 더 큰 것을 찾아 기호를 선택하세요.",
                style_role="question",
                x=72.0,
                y=26.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice_box",
                prompt="",
                x=332.0,
                y=66.0,
                width=282.0,
                height=98.0,
                stroke="#8F6ED5",
                stroke_width=2.0,
                fill="#FFFFFF",
            ),
            TextSlot(
                id="slot.opt1",
                prompt="",
                text="① 4 × 93",
                style_role="diagram",
                x=362.0,
                y=103.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt2",
                prompt="",
                text="ㄴ 7 × 54",
                style_role="diagram",
                x=478.0,
                y=103.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.work1",
                prompt="",
                text="① 4 × 93 = 372",
                style_role="supporting",
                x=58.0,
                y=252.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.work2",
                prompt="",
                text="ㄴ 7 × 54 = 378",
                style_role="supporting",
                x=58.0,
                y=292.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.compare",
                prompt="",
                text="372 < 378",
                style_role="supporting",
                x=58.0,
                y=332.0,
                font_size=24,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("elementary", "multiplication", "comparison"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008562",
    "problem_type": "선택형 비교",
    "metadata": {"grade": 3, "subject": "수학", "topic": "곱셈 결과 비교"},
    "domain": {
        "objects": [
            {"id": "expr_1", "type": "multiplication", "text": "4 × 93"},
            {"id": "expr_2", "type": "multiplication", "text": "7 × 54"},
            {"id": "symbol_1", "type": "choice_symbol", "text": "①"},
            {"id": "symbol_2", "type": "choice_symbol", "text": "ㄴ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": "두 곱셈식의 계산 결과를 비교하여 더 큰 쪽에 대응하는 기호를 고르는 문제이다.",
            "plan": "각 식의 결과를 확인한 뒤 크기를 비교한다.",
            "execute": "화면에 제시된 결과를 바탕으로 두 값을 비교한다.",
            "review": "더 큰 결과에 대응하는 기호가 선택되었는지 확인한다.",
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_symbol", "description": "더 큰 계산 결과에 해당하는 기호"},
        "value": "ㄴ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008562",
    "problem_type": "선택형 비교",
    "inputs": {
        "target_label": "더 큰 계산 결과에 해당하는 기호",
        "unit": "",
        "quantities": {
            "expr_1": "4 × 93",
            "expr_2": "7 × 54",
            "result_1": 372,
            "result_2": 378,
            "choice_1": "①",
            "choice_2": "ㄴ",
        },
    },
    "given": [
        {"ref": "expr_1", "value": "4 × 93"},
        {"ref": "expr_2", "value": "7 × 54"},
        {"ref": "result_1", "value": 372},
        {"ref": "result_2", "value": 378},
    ],
    "target": {"ref": "answer.target", "type": "selected_symbol"},
    "method": "compare_and_select",
    "plan": [
        "각 곱셈식의 결과를 확인한다.",
        "두 결과의 크기를 비교한다.",
        "더 큰 결과에 대응하는 기호를 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "372 < 378", "value": True},
        {"id": "step.2", "expr": "더 큰 값에 해당하는 기호 선택", "value": "ㄴ"},
    ],
    "checks": [
        {"id": "check.1", "expr": "선택한 기호가 더 큰 결과와 일치하는지 확인", "expected": "ㄴ", "actual": "ㄴ", "pass": True},
        {"id": "check.2", "expr": "비교식이 성립하는지 확인", "expected": "372 < 378", "actual": "372 < 378", "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_symbol", "description": "더 큰 계산 결과에 해당하는 기호"},
        "value": "ㄴ",
        "unit": "",
    },
}
