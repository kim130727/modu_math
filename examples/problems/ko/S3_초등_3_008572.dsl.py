from modu_math.dsl import Canvas, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(width = 750, height = 350)
    regions = (
        Region(
            id="header",
            role="stem",
            flow="absolute",
            slot_ids=("question", "box_frame"),
        ),
        Region(
            id="main",
            role="diagram",
            flow="absolute",
            slot_ids=("boxed_3", "boxed_4", "inner_3", "inner_2", "inner_x", "inner_1", "inner_4", "mul_bar"),
        ),
        Region(
            id="choices",
            role="diagram",
            flow="absolute",
            slot_ids=("choice_1", "choice_2", "choice_3", "choice_4", "choice_5"),
        ),
        Region(
            id="footer",
            role="supporting",
            flow="absolute",
            slot_ids=(),
        ),
    )
    slots = (
        TextSlot(
            id="question",
            text="계산에서 □ 안의 두 수의 곱은 실제로 얼마를 나타낼까요?",
            font_size=26,
            prompt="",
            style_role="question",
            x=66.0,
            y=30.0,
        ),
        RectSlot(
            id="box_frame",
            prompt="",
            x = 245, y = 60, width = 240, height = 140, stroke="#EAB5C2",
            stroke_width=2.0,
            fill="#FFFFFF",
        ),
        RectSlot(id="boxed_3", prompt="", x = 350, y = 75, width = 30, height = 30, stroke="#777777", stroke_width=1.5),
        RectSlot(id="boxed_4", prompt="", x = 400, y = 120, width = 30, height = 30, stroke="#777777", stroke_width=1.5),
        TextSlot(id="inner_3", text = '3', font_size = 30, prompt="", style_role="diagram", x = 355, y = 100),
        TextSlot(id="inner_2", text = '2', font_size = 30, prompt="", style_role="diagram", x = 405, y = 100),
        TextSlot(id="inner_x", text = '×', font_size = 30, prompt="", style_role="diagram", x = 305, y = 145),
        TextSlot(id="inner_1", text = '1', font_size = 30, prompt="", style_role="diagram", x = 355, y = 145),
        TextSlot(id="inner_4", text = '4', font_size = 30, prompt="", style_role="diagram", x = 405, y = 145),
        LineSlot(id="mul_bar", prompt="", x1 = 285, y1 = 170, x2 = 440, y2 = 170, stroke="#555555", stroke_width=1.5),
        TextSlot(
            id="choice_1", text = '① 10', font_size = 30, prompt="", style_role="diagram", x = 175, y = 260),
        TextSlot(
            id="choice_2", text = '② 12', font_size = 30, prompt="", style_role="diagram", x = 335, y = 260),
        TextSlot(
            id="choice_3", text = '③ 100', font_size = 30, prompt="", style_role="diagram", x = 475, y = 260),
        TextSlot(
            id="choice_4", text = '④ 120', font_size = 30, prompt="", style_role="diagram", x = 335, y = 310),
        TextSlot(
            id="choice_5", text = '⑤ 1000', font_size = 30, prompt="", style_role="diagram", x = 175, y = 310),
        
    )
    return ProblemTemplate(
        id="S3_초등_3_008572",
        title="계산에서 □ 안의 두 수의 곱은 실제로 얼마를 나타낼까요?",
        canvas=canvas,
        regions=regions,
        slots=slots,
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008572",
    "problem_type": "multiple_choice",
    "metadata": {"grade": 3, "subject": "수학"},
    "domain": {
        "objects": ["자리값을 나타내는 숫자", "곱셈 도식", "객관식 선택지"],
        "relations": [],
        "problem_solving": {
            "understand": "도식 속 숫자가 무엇을 나타내는지 자리값 관점에서 해석한다.",
            "plan": "보이는 해설 문장을 참고해 곱의 실제 의미를 이해한다.",
            "execute": "선택지 중 해설과 일치하는 값을 찾는다.",
            "review": "정답 표시와 해설 문장이 서로 맞는지 확인한다.",
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "도식이 실제로 나타내는 곱의 값"},
        "value": 120,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008572",
    "problem_type": "multiple_choice",
    "inputs": {
        "target_label": "도식이 실제로 나타내는 곱의 값",
        "unit": "",
        "quantities": {
            "expression_meaning": "3은 30, 4는 4를 나타낸다.",
            "visible_result": "30 × 4 = 120",
            "choices": [10, 12, 100, 120, 1000],
        },
    },
    "given": [
        {"ref": "diagram", "value": "3은 30, 4는 4를 나타낸다."},
        {"ref": "choices", "value": [10, 12, 100, 120, 1000]},
    ],
    "target": {"ref": "answer.target", "type": "selected_option"},
    "method": "compare_and_select",
    "plan": [
        "도식 속 숫자의 자리값을 해석한다.",
        "해설 문장에 인쇄된 계산식을 확인한다.",
        "정답 선택지와 계산 결과를 대응시킨다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "자리값 해석", "value": "3 → 30, 4 → 4"},
        {"id": "step.2", "expr": "곱 계산", "value": "30 × 4 = 120"},
        {"id": "step.3", "expr": "선택지 대응", "value": "④"},
    ],
    "checks": [
        {"id": "check.1", "expr": "120이 선택지에 존재하는지 확인", "expected": True, "actual": True, "pass": True},
        {"id": "check.2", "expr": "정답 값 일치", "expected": 120, "actual": 120, "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "도식이 실제로 나타내는 곱의 값"},
        "value": 120,
        "unit": "",
    },
}
