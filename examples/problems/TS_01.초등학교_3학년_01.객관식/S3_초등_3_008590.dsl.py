from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008590",
        title="문제를 바르게 설명한 사람을 선택하세요.",
        canvas=Canvas(width=840, height=630, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1", "slot.eq.bg", "slot.eq.text", "slot.eq.blank1", "slot.eq.blank2",
                    "slot.opt1.bubble", "slot.opt1.text", "slot.opt1.face.head", "slot.opt1.face.body", "slot.opt1.face.eye1", "slot.opt1.face.eye2", "slot.opt1.face.mouth", "slot.opt1.name",
                    "slot.opt2.bubble", "slot.opt2.text", "slot.opt2.face.head", "slot.opt2.face.body", "slot.opt2.face.eye1", "slot.opt2.face.eye2", "slot.opt2.face.mouth", "slot.opt2.name",
                    "slot.opt3.bubble", "slot.opt3.text", "slot.opt3.face.head", "slot.opt3.face.body", "slot.opt3.face.eye1", "slot.opt3.face.eye2", "slot.opt3.face.mouth", "slot.opt3.name",
                ),
            ),
        ),
        slots=(
            TextSlot(id="slot.q1", prompt="", text="57. 문제를 바르게 설명한 사람을 선택하세요.", style_role="question", x=16.0, y=34.0, font_size=28),
            RectSlot(id="slot.eq.bg", prompt="", x=275.0, y=47.0, width=390.0, height=78.0),
            TextSlot(id="slot.eq.text", prompt="", text="68 ÷ 5 = □ ... □", style_role="question", x=350.0, y=95.0, font_size=28),
            RectSlot(id="slot.eq.blank1", prompt="", x=490.0, y=74.0, width=28.0, height=28.0),
            RectSlot(id="slot.eq.blank2", prompt="", x=568.0, y=74.0, width=28.0, height=28.0),

            RectSlot(id="slot.opt1.bubble", prompt="", x=150.0, y=165.0, width=145.0, height=105.0),
            TextSlot(id="slot.opt1.text", prompt="", text="몫은\n13이야.", style_role="question", x=182.0, y=198.0, font_size=28),
            CircleSlot(id="slot.opt1.face.head", prompt="", cx=209.0, cy=325.0, r=24.0, fill="#F3C0AD"),
            RectSlot(id="slot.opt1.face.body", prompt="", x=197.0, y=342.0, width=24.0, height=34.0, rx=8.0, ry=8.0, fill="#D7A0D7", stroke="#D7A0D7"),
            CircleSlot(id="slot.opt1.face.eye1", prompt="", cx=203.0, cy=321.0, r=2.5, fill="#222222"),
            CircleSlot(id="slot.opt1.face.eye2", prompt="", cx=215.0, cy=321.0, r=2.5, fill="#222222"),
            LineSlot(id="slot.opt1.face.mouth", prompt="", x1=203.0, y1=331.0, x2=215.0, y2=331.0, stroke="#C36A6A", stroke_dasharray=""),
            TextSlot(id="slot.opt1.name", prompt="", text="형우", style_role="question", x=182.0, y=430.0, font_size=28),

            RectSlot(id="slot.opt2.bubble", prompt="", x=405.0, y=165.0, width=145.0, height=105.0),
            TextSlot(id="slot.opt2.text", prompt="", text="나머지는\n5보다 작아.", style_role="question", x=430.0, y=198.0, font_size=28),
            CircleSlot(id="slot.opt2.face.head", prompt="", cx=464.0, cy=325.0, r=24.0, fill="#F3C0AD"),
            RectSlot(id="slot.opt2.face.body", prompt="", x=452.0, y=342.0, width=24.0, height=34.0, rx=8.0, ry=8.0, fill="#8ED7E6", stroke="#8ED7E6"),
            CircleSlot(id="slot.opt2.face.eye1", prompt="", cx=458.0, cy=321.0, r=2.5, fill="#222222"),
            CircleSlot(id="slot.opt2.face.eye2", prompt="", cx=470.0, cy=321.0, r=2.5, fill="#222222"),
            LineSlot(id="slot.opt2.face.mouth", prompt="", x1=458.0, y1=331.0, x2=470.0, y2=331.0, stroke="#C36A6A", stroke_dasharray=""),
            TextSlot(id="slot.opt2.name", prompt="", text = '희영', style_role="question", x=438.0, y=430.0, font_size=28),

            RectSlot(id="slot.opt3.bubble", prompt="", x=660.0, y=165.0, width=145.0, height=105.0),
            TextSlot(id="slot.opt3.text", prompt="", text="나누어떨어지지\n않아.", style_role="question", x=684.0, y=198.0, font_size=28),
            CircleSlot(id="slot.opt3.face.head", prompt="", cx=719.0, cy=325.0, r=24.0, fill="#F3C0AD"),
            RectSlot(id="slot.opt3.face.body", prompt="", x=707.0, y=342.0, width=24.0, height=34.0, rx=8.0, ry=8.0, fill="#F2C66D", stroke="#F2C66D"),
            CircleSlot(id="slot.opt3.face.eye1", prompt="", cx=713.0, cy=321.0, r=2.5, fill="#222222"),
            CircleSlot(id="slot.opt3.face.eye2", prompt="", cx=725.0, cy=321.0, r=2.5, fill="#222222"),
            LineSlot(id="slot.opt3.face.mouth", prompt="", x1=713.0, y1=331.0, x2=725.0, y2=331.0, stroke="#C36A6A", stroke_dasharray=""),
            TextSlot(id="slot.opt3.name", prompt="", text = '성태', style_role="question", x=693.0, y=430.0, font_size=28),
        ),
        diagrams=(), groups=(), constraints=(), tags=("초등", "수학", "나눗셈", "몫", "나머지", "선택형"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008590",
    "problem_type": "division_explanation_choice",
    "metadata": {"language": "ko", "question": "문제를 바르게 설명한 사람을 선택하는 문항", "instruction": "68 ÷ 5의 결과를 설명한 내용 중 맞는 사람을 선택하세요."},
    "domain": {
        "objects": [
            {"id": "obj.dividend", "type": "number", "value": 68},
            {"id": "obj.divisor", "type": "number", "value": 5},
            {"id": "obj.person.left", "type": "person", "name": "형우"},
            {"id": "obj.person.middle", "type": "person", "name": "희영"},
            {"id": "obj.person.right", "type": "person", "name": "성태"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {"given_refs": ["obj.dividend", "obj.divisor"], "target_ref": "answer.target", "condition_refs": ["rel.choose_correct_explanation"]},
            "plan": {"method": "division_result_check", "description": "몫과 나머지의 성질을 이용해 맞는 설명을 고른다."},
            "execute": {"expected_operations": ["compute_quotient_remainder", "check_statements", "select_person"]},
            "review": {"check_methods": ["remainder_less_than_divisor", "selected_person_match"]},
        },
    },
    "answer": {"blanks": [], "choices": [], "answer_key": [], "target": {"type": "person_selection", "description": "문제를 바르게 설명한 사람"}, "value": "성태", "unit": ""},
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008590",
    "problem_type": "division_explanation_choice",
    "inputs": {"total_ticks": 0, "target_label": "문제를 바르게 설명한 사람", "target_ticks": 0, "target_count": 1, "unit": ""},
    "given": [
        {"ref": "obj.dividend", "value": 68},
        {"ref": "obj.divisor", "value": 5},
        {"ref": "obj.person.left", "value": "형우"},
        {"ref": "obj.person.middle", "value": "희영"},
        {"ref": "obj.person.right", "value": "성태"},
    ],
    "target": {"ref": "answer.target", "type": "person_selection"},
    "method": "division_result_check",
    "plan": ["68 ÷ 5의 몫과 나머지를 구한다.", "세 설명과 비교하여 맞는 사람을 고른다."],
    "steps": [
        {"id": "step.1", "expr": "68 ÷ 5", "value": {"quotient": 13, "remainder": 3}},
        {"id": "step.2", "expr": "나머지 < 나누는 수", "value": True},
        {"id": "step.3", "expr": "선택한 사람", "value": "성태"},
    ],
    "checks": [
        {"id": "check.1", "expr": "68 = 5 × 13 + 3", "expected": True, "actual": True, "pass": True},
        {"id": "check.2", "expr": "3 < 5", "expected": True, "actual": True, "pass": True},
    ],
    "answer": {"blanks": [], "choices": [], "answer_key": [], "target": {"type": "person_selection", "description": "문제를 바르게 설명한 사람"}, "value": "성태", "unit": ""},
}
