from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008573",
        title="계산 결과가 큰 것부터 순서 고르기",
        canvas=Canvas(width = 735, height = 325, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_text",),
            ),
            Region(
                id="region.center_box",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.main_box",
                    "slot.expr_g",
                    "slot.expr_n",
                    "slot.expr_d",
                    "slot.expr_r",
                ),
            ),
            Region(
                id="region.choices",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.choice1",
                    "slot.choice2",
                    "slot.choice3",
                    "slot.choice4",
                    "slot.choice5",
                ),
            ),
            Region(
                id="region.support",
                role="supporting",
                flow="absolute",
                slot_ids=( ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q_text",
                prompt="",
                text="계산 결과가 큰 것부터 차례대로 나타낸 것을 고르세요.",
                style_role="question",
                x=64.0,
                y=28.0,
                font_size=26,
            ),
            RectSlot(
                id="slot.main_box",
                prompt="",
                x = 155, y = 65, width = 420, height = 130, stroke="#EAB5C2",
                stroke_width=2.0,
                fill="#FFFFFF",
            ),
            TextSlot(
                id="slot.expr_g",
                prompt="",
                text = 'ㄱ 42 × 83', style_role="diagram",
                x = 200, y = 110, font_size = 25),
            TextSlot(
                id="slot.expr_n",
                prompt="",
                text = 'ㄴ 58 × 55', style_role="diagram",
                x = 375, y = 105, font_size = 25),
            TextSlot(
                id="slot.expr_d",
                prompt="",
                text = 'ㄷ 67 × 54', style_role="diagram",
                x = 200, y = 160, font_size = 25),
            TextSlot(
                id="slot.expr_r",
                prompt="",
                text = 'ㄹ 91 × 37', style_role="diagram",
                x = 375, y = 155, font_size = 25),
            TextSlot(
                id="slot.choice1",
                prompt="",
                text="① ㄱ, ㄷ, ㄴ, ㄹ",
                style_role="diagram",
                x=96.0,
                y=242.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.choice2",
                prompt="",
                text="② ㄴ, ㄱ, ㄷ, ㄹ",
                style_role="diagram",
                x=316.0,
                y=242.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.choice3",
                prompt="",
                text="③ ㄷ, ㄱ, ㄹ, ㄴ",
                style_role="diagram",
                x=536.0,
                y=242.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.choice4",
                prompt="",
                text="④ ㄷ, ㄱ, ㄴ, ㄹ",
                style_role="diagram",
                x=206.0,
                y=278.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.choice5",
                prompt="",
                text="⑤ ㄹ, ㄷ, ㄴ, ㄷ",
                style_role="diagram",
                x=446.0,
                y=278.0,
                font_size=24,
            ),
            
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008573",
    "problem_type": "순서 고르기",
    "metadata": {"grade": 3, "subject": "수학", "visible_answer": "③"},
    "domain": {
        "objects": [
            {"id": "expr_g", "type": "multiplication", "text": "42 × 83"},
            {"id": "expr_n", "type": "multiplication", "text": "58 × 55"},
            {"id": "expr_d", "type": "multiplication", "text": "67 × 54"},
            {"id": "expr_r", "type": "multiplication", "text": "91 × 37"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": "각 곱셈식의 계산 결과를 비교하여 큰 순서대로 배열하는 문제이다.",
            "plan": "네 식의 결과값을 비교하여 내림차순 순서를 구한다.",
            "execute": "가장 큰 값부터 기호 순서를 정해 보기와 대조한다.",
            "review": "선택한 보기와 계산 결과의 내림차순이 일치하는지 확인한다.",
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "큰 값부터의 기호 순서"},
        "value": "③",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008573",
    "problem_type": "순서 고르기",
    "inputs": {
        "target_label": "큰 값부터의 기호 순서",
        "unit": "",
        "quantities": {
            "ㄱ": 3486,
            "ㄴ": 3190,
            "ㄷ": 3618,
            "ㄹ": 3367,
        },
    },
    "given": [
        {"ref": "expr_g", "value": "42 × 83 = 3486"},
        {"ref": "expr_n", "value": "58 × 55 = 3190"},
        {"ref": "expr_d", "value": "67 × 54 = 3618"},
        {"ref": "expr_r", "value": "91 × 37 = 3367"},
    ],
    "target": {"ref": "answer.target", "type": "selected_option"},
    "method": "sort_descending_and_match_choice",
    "plan": ["값을 비교한다.", "내림차순으로 기호를 배열한다.", "보기와 일치하는 선택지를 고른다."],
    "steps": [
        {"id": "step.1", "expr": "결과값 비교", "value": "3618 > 3486 > 3367 > 3190"},
        {"id": "step.2", "expr": "기호 순서 변환", "value": "ㄷ, ㄱ, ㄹ, ㄴ"},
        {"id": "step.3", "expr": "보기 대조", "value": "③"},
    ],
    "checks": [
        {"id": "check.1", "expr": "내림차순 비교식 확인", "expected": "3618>3486>3367>3190", "actual": "3618>3486>3367>3190", "pass": True},
        {"id": "check.2", "expr": "정답 보기 일치", "expected": "③", "actual": "③", "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "큰 값부터의 기호 순서"},
        "value": "③",
        "unit": "",
    },
}

