from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    LineSlot,
    TextBoxSlot,
    RectSlot,
)


PROBLEM_ID = "P3_1_01_00040_02151"
PROBLEM_TITLE = "세 자리 수의 덧셈 계산"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=600,
            height=300,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.instruction",'konva_1785113315829_paste_130223_0', 'konva_1785113315829_paste_130223_1', 'konva_1785113315829_paste_130223_2', 'konva_1785113315829_paste_130223_3', 'konva_1785113315829_paste_130223_4', 'konva_1785113315829_paste_130223_5', 'konva_1785113315829_paste_130223_6', 'konva_1785113315829_paste_130223_7', 'konva_1785113315829_paste_130223_8', 'konva_1785113315829_paste_130223_9', 'konva_1785113315829_paste_135339_0', 'konva_1785113315829_paste_135339_1', 'konva_1785113315829_paste_135339_2', 'konva_1785113315829_paste_135339_3', 'konva_1785113315829_paste_135339_4', 'konva_1785113855579_rect_123138', 'konva_1785113855579_paste_146161_0', 'konva_1785113855579_paste_150620_0'),
            ),
            Region(
                id="region.problem_1",
                role="question",
                flow="absolute",
                slot_ids=(
                    
                ),
            ),
            Region(
                id="region.problem_2",
                role="question",
                flow="absolute",
                slot_ids=(
                    
                ),
            ),
        ),
        slots=(TextBoxSlot(
                id="slot.instruction",
                x=30,
                y=18,
                width=840,
                height=42,
                text="□ 안에 알맞은 수를 써넣으시오.",
                font_size=24,
                font_family='"Poor Story", "Noto Sans KR", sans-serif',
                fill="#202124",
                align="left",
                valign="middle",
            ),

            # (1) 449 + 275
            TextBoxSlot(id = 'konva_1785113315829_paste_130223_0', prompt = '', text = '(1)', x = 41.651, y = 73.394, font_size = 22, fill = '#202124', width = 34, height = 63, align = 'left', line_height = 1.25), TextBoxSlot(id = 'konva_1785113315829_paste_130223_1', prompt = '', text = '4 4 9', x = 79, y = 86, font_size = 25, fill = '#202124', width = 104, height = 40, align = 'center', line_height = 1.25), TextBoxSlot(id = 'konva_1785113315829_paste_130223_2', prompt = '', text = '+', x = 65, y = 122, font_size = 25, fill = '#202124', width = 24, height = 40, align = 'center', line_height = 1.25), TextBoxSlot(id = 'konva_1785113315829_paste_130223_3', prompt = '', text = '2 7 5', x = 82, y = 122, font_size = 25, fill = '#202124', width = 104, height = 40, align = 'center', line_height = 1.25), LineSlot(id = 'konva_1785113315829_paste_130223_4', prompt = '', x1 = 68.435, y1 = 164.0, x2 = 190.435, y2 = 164.0, stroke = '#111111', stroke_width = 1.6), TextBoxSlot(id = 'konva_1785113315829_paste_130223_5', prompt = '', text = '(2)', x = 212.512, y = 71.134, font_size = 22, fill = '#202124', width = 34, height = 63, align = 'left', line_height = 1.25), TextBoxSlot(id = 'konva_1785113315829_paste_130223_6', prompt = '', text = '3 7 3', x = 261.388, y = 87.435, font_size = 25, fill = '#202124', width = 104, height = 40, align = 'center', line_height = 1.25), TextBoxSlot(id = 'konva_1785113315829_paste_130223_7', prompt = '', text = '+', x = 247.388, y = 123.435, font_size = 25, fill = '#202124', width = 24, height = 40, align = 'center', line_height = 1.25), TextBoxSlot(id = 'konva_1785113315829_paste_130223_8', prompt = '', text = '4 6 8', x = 261.388, y = 123.435, font_size = 25, fill = '#202124', width = 104, height = 40, align = 'center', line_height = 1.25), LineSlot(id = 'konva_1785113315829_paste_130223_9', prompt = '', x1 = 249.388, y1 = 165.435, x2 = 371.388, y2 = 165.435, stroke = '#111111', stroke_width = 1.6), TextBoxSlot(id = 'konva_1785113315829_paste_135339_0', prompt = '', text = '(3)', x = 400.311, y = 70.746, font_size = 22, fill = '#202124', width = 34, height = 63, align = 'left', line_height = 1.25), TextBoxSlot(id = 'konva_1785113315829_paste_135339_1', prompt = '', text = '5 3 6', x = 449.187, y = 87.047, font_size = 25, fill = '#202124', width = 104, height = 40, align = 'center', line_height = 1.25), TextBoxSlot(id = 'konva_1785113315829_paste_135339_2', prompt = '', text = '+', x = 435.187, y = 123.047, font_size = 25, fill = '#202124', width = 24, height = 40, align = 'center', line_height = 1.25), TextBoxSlot(id = 'konva_1785113315829_paste_135339_3', prompt = '', text = '2 8 7', x = 449.187, y = 123.047, font_size = 25, fill = '#202124', width = 104, height = 40, align = 'center', line_height = 1.25), LineSlot(id = 'konva_1785113315829_paste_135339_4', prompt = '', x1 = 437.187, y1 = 165.047, x2 = 559.187, y2 = 165.047, stroke = '#111111', stroke_width = 1.6), RectSlot(id = 'konva_1785113855579_rect_123138', prompt = '', x = 81.789, y = 172.11, width = 83.828, height = 32.879, fill = '#ffffff', stroke = '#111827', stroke_width = 1.2), RectSlot(id = 'konva_1785113855579_paste_146161_0', prompt = '', x = 261.531, y = 174.591, width = 83.828, height = 32.879, fill = '#ffffff', stroke = '#111827', stroke_width = 1.2), RectSlot(id = 'konva_1785113855579_paste_150620_0', prompt = '', x = 447.861, y = 174.921, width = 83.828, height = 32.879, fill = '#ffffff', stroke = '#111827', stroke_width = 1.2)),
    )


PROBLEM_TEMPLATE = build_problem_template()


ANSWER = {
    "value": [724, 841, 823],
    "unit": "",
    "values": [724, 841, 823],
    "blanks": [
        {
            "id": "konva_1785113855579_rect_123138",
            "slot_id": "konva_1785113855579_rect_123138",
            "expected": 724,
        },
        {
            "id": "konva_1785113855579_paste_146161_0",
            "slot_id": "konva_1785113855579_paste_146161_0",
            "expected": 841,
        },
        {
            "id": "konva_1785113855579_paste_150620_0",
            "slot_id": "konva_1785113855579_paste_150620_0",
            "expected": 823,
        },
    ],
    "answer_key": [
        {"slot_id": "konva_1785113855579_rect_123138", "value": 724},
        {"slot_id": "konva_1785113855579_paste_146161_0", "value": 841},
        {"slot_id": "konva_1785113855579_paste_150620_0", "value": 823},
    ],
}

ADDITIONS = [
    ("addition.problem_1", "첫 번째 세로셈", 449, 275, 724),
    ("addition.problem_2", "두 번째 세로셈", 373, 468, 841),
    ("addition.problem_3", "세 번째 세로셈", 536, 287, 823),
]

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_answer_vertical_addition",
    "metadata": {
        "title": PROBLEM_TITLE,
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈 계산",
        "language": "ko-KR",
        "required_layout_ids": [
            "konva_1785113855579_rect_123138",
            "konva_1785113855579_paste_146161_0",
            "konva_1785113855579_paste_150620_0",
        ],
    },
    "domain": {
        "objects": [
            {
                "id": item[0],
                "type": "vertical_addition",
                "label": item[1],
                "first_addend": item[2],
                "second_addend": item[3],
                "sum": item[4],
            }
            for item in ADDITIONS
        ],
        "relations": [
            {
                "id": f"relation.problem_{index}_sum",
                "type": "sum_of",
                "subject": item[0],
                "values": [item[2], item[3]],
            }
            for index, item in enumerate(ADDITIONS, start=1)
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC

SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_answer_vertical_addition",
    "inputs": {
        "target_label": "각 세로셈의 계산 결과",
        "unit": "",
        "answer_type": "number_list",
        "quantities": {
            "problem_1": {"first_addend": 449, "second_addend": 275},
            "problem_2": {"first_addend": 373, "second_addend": 468},
            "problem_3": {"first_addend": 536, "second_addend": 287},
        },
        "conditions": [
            "일의 자리부터 차례대로 계산합니다.",
            "각 자리의 합이 10 이상이면 바로 윗자리로 1을 받아올림합니다.",
            "각 세로셈의 계산 결과를 네모 안에 씁니다.",
        ],
    },
    "given": [
        {"ref": item[0], "value": {"first_addend": item[2], "second_addend": item[3]}}
        for item in ADDITIONS
    ],
    "target": {"ref": "answer.vertical_addition_results", "type": "number_list"},
    "method": "각 세로셈에서 일의 자리부터 더하고 받아올림을 다음 자리 계산에 포함한다.",
    "plan": [
        "첫 번째 세로셈 449+275를 계산한다.",
        "두 번째 세로셈 373+468을 계산한다.",
        "세 번째 세로셈 536+287을 계산한다.",
    ],
    "steps": [
        {"id": "step.problem_1.compose_sum", "expr": "449 + 275", "value": 724, "explanation": "449와 275를 더하면 724입니다."},
        {"id": "step.problem_2.compose_sum", "expr": "373 + 468", "value": 841, "explanation": "373과 468을 더하면 841입니다."},
        {"id": "step.problem_3.compose_sum", "expr": "536 + 287", "value": 823, "explanation": "536과 287을 더하면 823입니다."},
    ],
    "checks": [
        {"id": "check.problem_1.total", "expr": "449 + 275", "expected": 724, "actual": 724, "pass": True},
        {"id": "check.problem_2.total", "expr": "373 + 468", "expected": 841, "actual": 841, "pass": True},
        {"id": "check.problem_3.total", "expr": "536 + 287", "expected": 823, "actual": 823, "pass": True},
    ],
    "answer": ANSWER,
    "understanding": {
        "summary": "세 자리 수 세로셈 세 개의 합을 구합니다.",
        "facts": [
            {"ref": item[0], "label": item[1], "value": {"first_addend": item[2], "second_addend": item[3]}, "unit": "", "source": "explicit"}
            for item in ADDITIONS
        ],
        "unknowns": [
            {"ref": "answer.vertical_addition_results", "label": "각 세로셈의 계산 결과", "unit": "", "source": "unknown"}
        ],
        "relation": {
            "type": "vertical_addition",
            "statement": "세 자리 수 세로셈 세 개를 각각 계산합니다.",
            "symbolic": "449+275, 373+468, 536+287",
            "uses": ["addition.problem_1", "addition.problem_2", "addition.problem_3"],
            "result": "answer.vertical_addition_results",
        },
    },
}

SEMANTIC_ANSWER = SOLVABLE["answer"]
