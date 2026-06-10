from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    LineSlot,
    CircleSlot,
    PathSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008641",
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
                    "slot.note.text",'slot.note.text.copy6'),
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
                x1 = 251, y1 = 382, x2 = 521, y2 = 272),
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
                text = '한 원에서 원의 지름은 모두 ( 같습니다, 다릅니다 ).', style_role="choice",
                x = 90, y = 540, font_size = 30),TextSlot(id = 'slot.q1.copy5', prompt = '', text = '지름을 재어 알맞은 말을 선택하세요.', x = 20, y = 100, font_size = 30, fill = '#111111'), TextSlot(id = 'slot.note.text.copy6', prompt = '', text = 'ㅇ', x = 365, y = 310, font_size = 25, fill = '#111111')),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008641",
    "problem_type": "concept_choice",
    "metadata": {
        "language": "ko",
        "question": "한 원에서 지름의 성질을 보고 알맞은 말을 고르는 문제",
        "instruction": "지름을 재어 알맞은 말을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.diameter.1", "type": "diameter", "owner": "은지"},
            {"id": "obj.diameter.2", "type": "diameter", "owner": "진아"},
            {"id": "obj.diameter.3", "type": "diameter", "owner": "현준"},
            {"id": "obj.center", "type": "center"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.diameter.1",
                    "obj.diameter.2",
                    "obj.diameter.3",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.diameter_equality"],
            },
            "plan": {
                "method": "concept_recognition",
                "description": "한 원에서 지름의 성질을 떠올려 알맞은 선택지를 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_diameter_property",
                    "compare_choice_words",
                ]
            },
            "review": {"check_methods": ["property_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_word",
            "description": "한 원에서 원의 지름은 모두 ( 같습니다, 다릅니다 )에서 알맞은 말",
        },
        "value": "같습니다",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008641",
    "problem_type": "concept_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "같습니다",
        "target_ticks": 0,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.diameter.1", "value": {"owner": "은지", "type": "diameter"}},
        {"ref": "obj.diameter.2", "value": {"owner": "진아", "type": "diameter"}},
        {"ref": "obj.diameter.3", "value": {"owner": "현준", "type": "diameter"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_word"},
    "method": "concept_recognition",
    "plan": [
        "한 원에서 지름의 성질을 확인한다.",
        "보기의 두 말 중 알맞은 말을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "한 원의 지름은 모두 같은 성질을 가진다.",
            "value": "같다",
        },
        {
            "id": "step.2",
            "expr": "선택지 ( 같습니다, 다릅니다 ) 중 알맞은 말 선택",
            "value": "같습니다",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "지름의 성질과 선택어가 일치하는가",
            "expected": "같습니다",
            "actual": "같습니다",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_word",
            "description": "한 원에서 원의 지름은 모두 ( 같습니다, 다릅니다 )에서 알맞은 말",
        },
        "value": "같습니다",
        "unit": "",
    },
}
