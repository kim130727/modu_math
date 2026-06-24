from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008802",
        title="고구마와 감자의 무게를 비교하는 방법",
        canvas=Canvas(width=952.0, height=602.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q3"),
            ),
            Region(
                id="region.dialogue_left",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.left.speech", "slot.left.name"),
            ),
            Region(
                id="region.dialogue_right",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.right.speech", "slot.right.name"),
            ),
            Region(id="region.footer", role="note", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 31. 고구마와 감자를 양손에 들어 보니 어느 것이 더 무거",
                style_role="question",
                x=12.0,
                y=24.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="운지 알 수 없었습니다. 고구마와 감자의 무게를 비교할 수 있는 방법을 바",
                style_role="question",
                x=12.0,
                y=58.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="르게 말한 사람을 선택해 보세요.",
                style_role="question",
                x=12.0,
                y=92.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.left.speech",
                prompt="",
                text="눈으로 크기를\n비교해 보면 크기가\n조금이라도 더 큰 것이\n더 무거워.",
                style_role="speech",
                x=116.0,
                y=164.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.left.name",
                prompt="",
                text="상규",
                style_role="label",
                x=304.0,
                y=448.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.right.speech",
                prompt="",
                text="저울의 양쪽 접시에\n고구마와 감자를 각각 올려\n접시가 아래로 내려온 것이\n더 무거워.",
                style_role="speech",
                x=606.0,
                y=164.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.right.name",
                prompt="",
                text="민하",
                style_role="label",
                x=568.0,
                y=448.0,
                font_size=28,
            ),
            CircleSlot(id="slot.left.face", prompt="", cx=330.0, cy=328.0, r=2.0, fill="#222222"),
            CircleSlot(id="slot.right.face", prompt="", cx=596.0, cy=328.0, r=2.0, fill="#222222"),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008802",
    "problem_type": "choice",
    "metadata": {
        "language": "ko",
        "question": "고구마와 감자의 무게를 비교할 수 있는 방법을 바르게 말한 사람을 선택하는 문제",
        "instruction": "바르게 말한 사람을 선택해 보세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.sweet_potato", "type": "food", "name": "고구마"},
            {"id": "obj.potato", "type": "food", "name": "감자"},
            {"id": "obj.sun_gyu", "type": "person", "name": "상규"},
            {"id": "obj.min_ha", "type": "person", "name": "민하"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.sweet_potato", "obj.potato", "obj.sun_gyu", "obj.min_ha"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_weight"],
            },
            "plan": {
                "method": "compare_by_scale",
                "description": "무게를 직접 비교할 수 있는 올바른 방법을 고른다.",
            },
            "execute": {
                "expected_operations": ["문장의 뜻 비교", "무게 비교 방법 확인", "올바른 사람 선택"]
            },
            "review": {"check_methods": ["방법이 무게 비교에 적절한지 확인"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_person",
            "description": "고구마와 감자의 무게를 비교하는 올바른 방법을 말한 사람",
        },
        "value": "민하",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008802",
    "problem_type": "choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "정답인 사람",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.sweet_potato", "value": {"name": "고구마"}},
        {"ref": "obj.potato", "value": {"name": "감자"}},
        {"ref": "obj.sun_gyu", "value": {"name": "상규"}},
        {"ref": "obj.min_ha", "value": {"name": "민하"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_person"},
    "method": "compare_by_scale",
    "plan": [
        "두 사람이 말한 방법이 무게 비교에 적절한지 확인한다.",
        "저울을 이용하는 방법이 올바른지 판단한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "상규의 방법은 눈으로 크기를 비교하는 방법이다.",
            "value": "부적절",
        },
        {
            "id": "step.2",
            "expr": "민하의 방법은 저울의 양쪽 접시에 각각 올려 무게를 비교하는 방법이다.",
            "value": "적절",
        },
        {"id": "step.3", "expr": "올바른 사람 선택", "value": "민하"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "저울을 사용해 무게를 비교하는 방법이 맞는가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선택된 사람이 민하인가",
            "expected": "민하",
            "actual": "민하",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_person",
            "description": "고구마와 감자의 무게를 비교하는 올바른 방법을 말한 사람",
        },
        "value": "민하",
        "unit": "",
    },
}
