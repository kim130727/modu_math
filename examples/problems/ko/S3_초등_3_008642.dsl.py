from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
    PathSlot,
TextBoxSlot)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008642",
        title="원의 지름",
        canvas=Canvas(width=940, height=640, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",'slot.q1.copy5')
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.circle",
                    "slot.center",
                    "slot.diameter.vertical",
                    "slot.diameter.green",
                    "slot.diameter.purple",
                    "slot.label.eunji",
                    "slot.label.jina",
                    "slot.label.hyeonjun",
                    "slot.note.arrow",
                    "slot.note.text",'slot.note.text.copy6', 'konva_1784612321567_paste_583821_0', 'konva_1784612321567_arrow_620234'),
            ),
            Region(
                id="region.choice",
                role="choice",
                flow="absolute",
                slot_ids=("slot.choice.box", "slot.choice.text"),
            ),
            Region(id="region.footer", role="footer", flow="absolute", slot_ids=()),
        ),
        slots=(TextSlot(
                id="slot.q1",
                prompt="",
                text = '은지, 진아, 현준이가 한 원에 지름을 그은 것입니다.', style_role="question",
                x = 20, y = 40, font_size = 30),
            CircleSlot(
                id="slot.circle", prompt="", cx = 385, cy = 325, r = 145, fill="none"
            ),
            CircleSlot(
                id="slot.center", prompt="", cx = 390, cy = 325, r = 5, fill="#d02aa6"
            ),
            LineSlot(
                id="slot.diameter.vertical",
                prompt="",
                x1 = 390, y1 = 183, x2 = 390, y2 = 468),
            LineSlot(
                id="slot.diameter.green",
                prompt="",
                x1 = 264, y1 = 246, x2 = 509, y2 = 401),
            LineSlot(
                id="slot.diameter.purple",
                prompt="",
                x1 = 251.124, y1 = 382.629, x2 = 521.124, y2 = 272.629),
            TextSlot(
                id="slot.label.eunji",
                prompt="",
                text = '은지', style_role="label",
                x = 360, y = 160, font_size = 30),
            TextSlot(
                id="slot.label.jina",
                prompt="",
                text = '진아', style_role="label",
                x = 525, y = 270, font_size = 30),
            TextSlot(
                id="slot.label.hyeonjun",
                prompt="",
                text = '현준', style_role="label",
                x = 515, y = 430, font_size = 30),
            PathSlot(
                id="slot.note.arrow",
                prompt="",
                d = 'M 605 325 C 555 305, 545 285, 495 260 C 475 245, 450 230, 430 215', stroke = '#111111', stroke_width = 2, transform = 'rotate(-390 625 327.5)'),
            TextSlot(
                id="slot.note.text",
                prompt="",
                text = '\n    \n        \n            \n                \n                    \n                        \n                            \n                                \n                                    지름은 모두\n                                    원의 중심을\n                                    지나요.\n                                  \n                              \n                          \n                      \n                  \n              \n          \n      \n  ', style_role="note",
                x = 615, y = 295, font_size = 25),
            RectSlot(
                id="slot.choice.box",
                prompt="",
                x = 10, y = 490, width = 760, height = 80),
            TextSlot(
                id="slot.choice.text",
                prompt="",
                text = '(무수히 많이 그릴 수 있습니다., 3개)', style_role="choice",
                x = 90, y = 540, font_size = 30),TextSlot(id = 'slot.q1.copy5', prompt = '', text = '지름을 재어 알맞은 말을 선택하세요.', x = 20, y = 100, font_size = 30, fill = '#111111'), TextSlot(id = 'slot.note.text.copy6', prompt = '', text = 'ㅇ', x = 365, y = 310, font_size = 25, fill = '#111111'), TextBoxSlot(id = 'konva_1784612321567_paste_583821_0', prompt = '', text = '지름은 모두 원의 중심을 지나요.', x = 653.761, y = 299.264, font_size = 30, fill = '#111827', width = 214.383, height = 121, align = 'left', line_height = 1.25), PathSlot(id = 'konva_1784612321567_arrow_620234', prompt = '', d = 'M 399.163 326.53 L 643.163 340.02 M 643.163 340.02 L 633.003 344.24 M 643.163 340.02 L 633.533 334.71', fill = 'none', stroke = '#111827', stroke_width = 1.2)),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008642",
    "problem_type": "conceptual_choice",
    "metadata": {
        "language": "ko",
        "question": "한 원에 지름을 몇 개 그을 수 있는지 알맞은 것을 선택하는 문제",
        "instruction": "알맞은 것을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.diameter", "type": "diameter", "count": "multiple"},
            {"id": "obj.center", "type": "center"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.center", "obj.diameter"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.diameter_through_center"],
            },
            "plan": {
                "method": "definition_check",
                "description": "지름의 정의를 확인해 한 원에 가능한 지름의 개수를 판단한다.",
            },
            "execute": {
                "expected_operations": ["identify_definition", "compare_choices"]
            },
            "review": {"check_methods": ["definition_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice",
            "description": "한 원에 지름을 몇 개 그을 수 있는지에 대한 알맞은 선택지",
        },
        "value": "무수히 많이 그을 수 있습니다.",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008642",
    "problem_type": "conceptual_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "한 원에 지름을 몇 개 그을 수 있는지",
        "target_ticks": 0,
        "target_count": 0,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.center", "value": {"type": "center"}},
        {"ref": "obj.diameter", "value": {"count": "multiple"}},
    ],
    "target": {"ref": "answer.target", "type": "choice"},
    "method": "definition_check",
    "plan": [
        "지름의 정의를 확인한다.",
        "한 원에 그을 수 있는 지름의 개수를 판단한다.",
        "보기와 일치하는 선택지를 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "지름은 원의 중심을 지나고 원 위의 두 점을 잇는 선분이다.",
            "value": "definition",
        },
        {
            "id": "step.2",
            "expr": "원의 중심을 지나는 방향은 여러 가지가 가능하다.",
            "value": "multiple",
        },
        {
            "id": "step.3",
            "expr": "따라서 한 원에 지름은 무수히 많이 그을 수 있다.",
            "value": "무수히 많이",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "지름이 중심을 지나는가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선택지가 정의와 일치하는가",
            "expected": "무수히 많이 그을 수 있습니다.",
            "actual": "무수히 많이 그을 수 있습니다.",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice",
            "description": "한 원에 지름을 몇 개 그을 수 있는지에 대한 알맞은 선택지",
        },
        "value": "무수히 많이 그을 수 있습니다.",
        "unit": "",
    },
}
