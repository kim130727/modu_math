from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008867",
        title="2L에 더 가깝게 어림한 친구",
        canvas=Canvas(width=945.0, height=468.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q3", "slot.q4"),
            ),
            Region(
                id="region.table",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.table.outer",
                    "slot.table.head_left",
                    "slot.table.head_right",
                    "slot.table.body_left",
                    "slot.table.body_right",
                ),
            ),
            Region(id="region.choice", role="diagram", flow="absolute", slot_ids=("slot.choice",)),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="18.",
                style_role="question",
                x=8.0,
                y=18.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="민재와 수현이가 2L의 물을 어림하여 각각의 물통에 담았습니다.",
                style_role="question",
                x=41.0,
                y=18.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="담은 물의 양을 실제로 재었더니 다음과 같습니다. 2L에 더 가깝게 어림한 친구",
                style_role="question",
                x=17.0,
                y=53.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q4",
                prompt="",
                text="는 누구인지 선택하세요.",
                style_role="question",
                x=8.0,
                y=88.0,
                font_size=28,
            ),
            RectSlot(id="slot.table.outer", prompt="", x=305.0, y=122.0, width=353.0, height=97.0),
            RectSlot(
                id="slot.table.head_left", prompt="", x=305.0, y=122.0, width=176.5, height=48.5
            ),
            RectSlot(
                id="slot.table.head_right", prompt="", x=481.5, y=122.0, width=176.5, height=48.5
            ),
            RectSlot(
                id="slot.table.body_left", prompt="", x=305.0, y=170.5, width=176.5, height=48.5
            ),
            RectSlot(
                id="slot.table.body_right", prompt="", x=481.5, y=170.5, width=176.5, height=48.5
            ),
            TextSlot(
                id="slot.table.head_text_left",
                prompt="",
                text="민재",
                style_role="label",
                x=376.0,
                y=153.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.head_text_right",
                prompt="",
                text="수현",
                style_role="label",
                x=550.0,
                y=153.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.body_text_left",
                prompt="",
                text="1850 mL",
                style_role="label",
                x=345.0,
                y=200.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.body_text_right",
                prompt="",
                text="2L 200mL",
                style_role="label",
                x=505.0,
                y=200.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="（ 민재 , 수현 ）",
                style_role="label",
                x=753.0,
                y=245.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008867",
    "problem_type": "비교",
    "metadata": {
        "language": "ko",
        "question": "2L에 더 가깝게 어림한 친구를 찾는 문제",
        "instruction": "2L에 더 가깝게 어림한 친구는 누구인지 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.target_amount", "type": "quantity", "label": "2L"},
            {"id": "obj.minjai_amount", "type": "quantity", "label": "1850mL"},
            {"id": "obj.suhyeon_amount", "type": "quantity", "label": "2L 200mL"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.target_amount", "obj.minjai_amount", "obj.suhyeon_amount"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_distance"],
            },
            "plan": {
                "method": "같은 기준량과의 차이를 비교한다",
                "description": "2L와 각 물의 양의 차이를 구해 더 작은 쪽을 고른다.",
            },
            "execute": {"expected_operations": ["단위 비교", "차이 계산", "크기 비교"]},
            "review": {"check_methods": ["차이가 더 작은지 확인", "기준량에 더 가까운지 확인"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "2L에 더 가깝게 어림한 친구"},
        "value": "민재",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008867",
    "problem_type": "비교",
    "inputs": {
        "total_ticks": 1,
        "target_label": "2L에 더 가깝게 어림한 친구",
        "target_ticks": 1,
        "target_count": 2,
        "unit": "mL",
    },
    "given": [
        {"ref": "obj.target_amount", "value": "2L"},
        {"ref": "obj.minjai_amount", "value": "1850mL"},
        {"ref": "obj.suhyeon_amount", "value": "2L 200mL"},
    ],
    "plan": "2L와 각 학생의 물의 양의 차이를 비교한다.",
    "steps": [
        {"id": "step.1", "expr": "2L = 2000mL", "value": 2000},
        {"id": "step.2", "expr": "2000mL - 1850mL", "value": 150},
        {"id": "step.3", "expr": "2L 200mL - 2L", "value": 200},
        {"id": "step.4", "expr": "150 < 200", "value": True},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "민재의 차이가 수현의 차이보다 작은가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "2L에 더 가깝게 어림한 친구"},
        "value": "민재",
        "unit": "",
    },
}
