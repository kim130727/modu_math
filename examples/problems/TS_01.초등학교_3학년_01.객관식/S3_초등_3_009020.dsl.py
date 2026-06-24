from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_009020",
        title="반직선과 직선의 다른 점을 바르게 말한 사람의 이름을 선택해 보세요.",
        canvas=Canvas(width=860, height=470, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.box", "slot.no", "slot.title"),
            ),
            Region(
                id="region.characters",
                role="body",
                flow="absolute",
                slot_ids=(
                    "slot.bubble.left",
                    "slot.bubble.right",
                    "slot.name.left_box",
                    "slot.name.left",
                    "slot.name.right_box",
                    "slot.name.right",
                    "slot.choice",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            RectSlot(id="slot.box", prompt="", x=8.0, y=14.0, width=14.0, height=14.0),
            TextSlot(
                id="slot.no",
                prompt="",
                text="58.",
                style_role="question",
                x=32.0,
                y=27.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.title",
                prompt="",
                text="반직선과 직선의 다른 점을 바르게 말한 사람의 이름을 선택해 보세요.",
                style_role="question",
                x=72.0,
                y=27.0,
                font_size=28,
            ),
            RectSlot(id="slot.bubble.left", prompt="", x=120.0, y=58.0, width=220.0, height=86.0),
            RectSlot(id="slot.bubble.right", prompt="", x=585.0, y=54.0, width=210.0, height=92.0),
            TextSlot(
                id="slot.bubble.left.text",
                prompt="",
                text="반직선은 한쪽으로\n늘어나고 직선은 양쪽으로\n늘어남.",
                style_role="question",
                x=146.0,
                y=90.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.bubble.right.text",
                prompt="",
                text="반직선은 시작점이\n없지만, 직선은\n시작점이 없어.",
                style_role="question",
                x=604.0,
                y=86.0,
                font_size=24,
            ),
            RectSlot(id="slot.name.left_box", prompt="", x=293.0, y=168.0, width=44.0, height=24.0),
            TextSlot(
                id="slot.name.left",
                prompt="",
                text="성진",
                style_role="question",
                x=304.0,
                y=186.0,
                font_size=22,
            ),
            RectSlot(
                id="slot.name.right_box", prompt="", x=458.0, y=168.0, width=44.0, height=24.0
            ),
            TextSlot(
                id="slot.name.right",
                prompt="",
                text="희경",
                style_role="question",
                x=469.0,
                y=186.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 성진 , 희경 )",
                style_role="question",
                x=344.0,
                y=230.0,
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
    "problem_id": "S3_초등_3_009020",
    "problem_type": "개념판별",
    "metadata": {
        "language": "ko",
        "question": "반직선과 직선의 다른 점을 바르게 말한 사람을 고르는 문제",
        "instruction": "바르게 말한 사람의 이름을 선택한다.",
        "points": 5,
    },
    "domain": {
        "objects": [
            {"id": "obj.ray", "type": "geometry_object", "name": "반직선"},
            {"id": "obj.line", "type": "geometry_object", "name": "직선"},
            {"id": "obj.sungjin", "type": "person", "name": "성진"},
            {"id": "obj.hiukyeong", "type": "person", "name": "희경"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.ray", "obj.line", "obj.sungjin", "obj.hiukyeong"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_ray_line", "rel.answer_choice"],
            },
            "plan": {
                "method": "개념판별",
                "description": "반직선과 직선의 성질 설명이 맞는지를 비교하여 바르게 말한 사람을 고른다.",
            },
            "execute": {
                "expected_operations": ["compare_geometric_properties", "select_correct_person"]
            },
            "review": {"check_methods": ["statement_consistency_check", "answer_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "person_name",
            "description": "반직선과 직선의 다른 점을 바르게 말한 사람의 이름",
        },
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009020",
    "problem_type": "개념판별",
    "inputs": {
        "total_ticks": 1,
        "target_label": "바르게 말한 사람의 이름",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.ray", "value": {"name": "반직선"}},
        {"ref": "obj.line", "value": {"name": "직선"}},
        {"ref": "obj.sungjin", "value": {"name": "성진"}},
        {"ref": "obj.hiukyeong", "value": {"name": "희경"}},
    ],
    "target": {"ref": "answer.target", "type": "person_name"},
    "method": "개념판별",
    "plan": ["반직선과 직선의 성질 설명을 비교한다.", "맞는 설명을 한 사람을 고른다."],
    "steps": [
        {"id": "step.1", "expr": "반직선과 직선의 차이를 비교한다.", "value": "시작점의 유무"},
        {"id": "step.2", "expr": "바르게 말한 사람을 선택한다.", "value": "성진"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 이름이 해설의 결론과 일치하는가",
            "expected": "성진",
            "actual": "성진",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "person_name",
            "description": "반직선과 직선의 다른 점을 바르게 말한 사람의 이름",
        },
        "value": 1,
        "unit": "",
    },
}
