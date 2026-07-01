from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PathSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
    ImageSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008787",
        title="들이가 더 많은 용기 고르기",
        canvas=Canvas(width=940, height=470, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qtext1", "slot.qtext2", "slot.choice", "slot.inserted.image.1"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qtext1",
                prompt="",
                text="우유병에 물을 가득 채운 후 페트병에 옮겨 담았습니다.",
                style_role="question",
                x=47,
                y=54,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.qtext2",
                prompt="",
                text="그림과 같이 물이 채워졌을 때 알맞은 말을 선택하세요.",
                style_role="question",
                x=47,
                y=97,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 유우병 , 페트병 )의 들이가 더 많습니다.",
                style_role="question",
                x=200,
                y=429,
                font_size=28,
                fill="#111111",
            ),
            ImageSlot(
                id="slot.inserted.image.1",
                prompt="",
                href="data:image/png;base64,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",
                x=325,
                y=125,
                width=230,
                height=260,
                preserve_aspect_ratio="xMidYMid meet",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("비교", "들이", "선택형"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008787",
    "problem_type": "capacity_comparison",
    "metadata": {
        "language": "ko",
        "question": "그림을 보고 더 많은 들이를 가진 용기를 선택하는 문제",
        "instruction": "알맞은 말을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.yuubyeong", "type": "container", "name": "유우병"},
            {"id": "obj.petbottle", "type": "container", "name": "페트병"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.yuubyeong", "obj.petbottle"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_capacity"],
            },
            "plan": {
                "method": "compare_capacity_from_illustration",
                "description": "그림과 해설을 바탕으로 더 많은 들이를 가진 용기를 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_containers",
                    "compare_capacity",
                    "select_more_capacity",
                ]
            },
            "review": {"check_methods": ["choice_matches_explanation"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_container", "description": "문장 괄호 안에 들어갈 알맞은 말"},
        "value": "페트병",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008787",
    "problem_type": "capacity_comparison",
    "inputs": {
        "total_ticks": 1,
        "target_label": "더 많은 들이",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.yuubyeong", "value": {"name": "유우병"}},
        {"ref": "obj.petbottle", "value": {"name": "페트병"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_container"},
    "method": "compare_capacity_from_illustration",
    "plan": ["그림과 해설을 보고 더 많은 들이를 가진 용기를 고른다."],
    "steps": [
        {
            "id": "step.1",
            "expr": "유우병에 가득 채운 물이 페트병에 가득 차는지 확인한다.",
            "value": False,
        },
        {
            "id": "step.2",
            "expr": "페트병에 가득 차지 않으므로 더 많은 들이를 가진 용기를 선택한다.",
            "value": "페트병",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 용기가 해설의 정답과 같은가",
            "expected": "페트병",
            "actual": "페트병",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_container", "description": "문장 괄호 안에 들어갈 알맞은 말"},
        "value": "페트병",
        "unit": "",
    },
}
