from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, LineSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008838",
        title="가장 가벼운 채소 찾기",
        canvas=Canvas(width=940, height=524, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_text1", "slot.q_text2"),
            ),
            Region(
                id="region.diagram.left",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.left.center",
                    "slot.left.obj.onion",
                    "slot.left.obj.nasu",
                ),
            ),
            Region(
                id="region.diagram.right",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.right.center",
                    "slot.right.obj.cucumber",
                    "slot.right.obj.onion",
                ),
            ),
            Region(
                id="region.choice",
                role="body",
                flow="absolute",
                slot_ids=("slot.choice.1", "slot.choice.2"),
            ),
            Region(id="region.explain", role="body", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q_text1",
                prompt="",
                text="양파, 가지, 오이 중에서 가장 가벼운 채소가 무엇인지 알아보는 방법을",
                style_role="question",
                x=27.954,
                y=37.661,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.q_text2",
                prompt="",
                text="설명하고 있습니다. 알맞은 말을 선택하세요.",
                style_role="question",
                x=25.813,
                y=78.795,
                font_size=28,
                fill="#111111",
            ),
            CircleSlot(id="slot.left.center", prompt="", cx=300.0, cy=150.0, r=5.0, fill="#C9D6E6"),
            CircleSlot(
                id="slot.left.obj.onion", prompt="", cx=245.0, cy=136.0, r=12.0, fill="#F4C06B"
            ),
            CircleSlot(
                id="slot.left.obj.nasu", prompt="", cx=356.0, cy=134.0, r=11.0, fill="#8F4DB8"
            ),
            CircleSlot(
                id="slot.right.center", prompt="", cx=620.0, cy=150.0, r=5.0, fill="#C9D6E6"
            ),
            CircleSlot(
                id="slot.right.obj.cucumber", prompt="", cx=570.0, cy=134.0, r=11.0, fill="#60B854"
            ),
            CircleSlot(
                id="slot.right.obj.onion", prompt="", cx=675.0, cy=136.0, r=12.0, fill="#F4C06B"
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="양파와 가지 중 ( 양파 , 가지 )가 더 가볍고,",
                style_role="question",
                x=196.527,
                y=421.424,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text="오이와 양파 중 ( 오이 , 양파 )가 더 가볍습니다.",
                style_role="question",
                x=196.527,
                y=463.424,
                font_size=28,
                fill="#111111",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008838",
    "problem_type": "비교",
    "metadata": {
        "language": "ko",
        "question": "양파, 가지, 오이 중에서 가장 가벼운 채소가 무엇인지 알아보는 방법을 설명하고 있습니다.",
        "instruction": "알맞은 말을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.onion", "type": "채소", "name": "양파"},
            {"id": "obj.nasu", "type": "채소", "name": "가지"},
            {"id": "obj.cucumber", "type": "채소", "name": "오이"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.onion",
                    "obj.nasu",
                    "obj.cucumber",
                    "rel.compare_1",
                    "rel.compare_2",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_1", "rel.compare_2"],
            },
            "plan": {
                "method": "무게 비교",
                "description": "저울의 기울기와 문장을 읽어 더 가벼운 채소를 찾고, 그 결과를 바탕으로 다음 비교 대상을 정한다.",
            },
            "execute": {
                "expected_operations": [
                    "비교 결과 읽기",
                    "더 가벼운 대상 선택하기",
                    "다음 비교 대상 확인하기",
                ]
            },
            "review": {
                "check_methods": ["그림과 문장의 일치 확인", "더 가벼운 대상이 맞는지 다시 보기"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "가장 가벼운 채소",
            "description": "양파, 가지, 오이 중 가장 가벼운 채소를 찾기",
        },
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008838",
    "problem_type": "비교",
    "inputs": {
        "total_ticks": 2,
        "target_label": "가장 가벼운 채소",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.onion", "value": "양파"},
        {"ref": "obj.nasu", "value": "가지"},
        {"ref": "obj.cucumber", "value": "오이"},
        {"ref": "rel.compare_1", "value": "양파와 가지 비교"},
        {"ref": "rel.compare_2", "value": "오이와 양파 비교"},
    ],
    "target": {"ref": "answer.target", "type": "가장 가벼운 채소"},
    "method": "무게 비교",
    "plan": [
        "저울과 문장을 보고 더 가벼운 채소를 비교해 나간다.",
        "두 비교 결과를 연결하여 가장 가벼운 채소를 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "양파와 가지를 비교한다.", "value": "양파가 더 무거움"},
        {"id": "step.2", "expr": "오이와 양파를 비교한다.", "value": "양파가 더 무거움"},
        {
            "id": "step.3",
            "expr": "비교 결과를 종합한다.",
            "value": "가지와 오이 중 더 가벼운 쪽을 추가로 비교해야 함",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "문장과 그림의 비교 방향이 일치하는지 확인한다.",
            "expected": "일치",
            "actual": "일치",
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "정답 표기가 본문 바깥의 별도 텍스트로 유지되는지 확인한다.",
            "expected": "유지",
            "actual": "유지",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "가장 가벼운 채소",
            "description": "양파, 가지, 오이 중 가장 가벼운 채소를 찾기",
        },
        "value": 0,
        "unit": "",
    },
}
