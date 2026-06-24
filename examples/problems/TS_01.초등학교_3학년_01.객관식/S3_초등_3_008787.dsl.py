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
                slot_ids=(
                    "slot.qno",
                    "slot.qtext1",
                    "slot.qtext2",
                    "slot.label.yuubyeong",
                    "slot.label.petbottle",
                    "slot.choice",
                ),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.yuubyeong.body",
                    "slot.diagram.yuubyeong.water",
                    "slot.diagram.yuubyeong.cap",
                    "slot.diagram.yuubyeong.spout",
                    "slot.diagram.petbottle.body",
                    "slot.diagram.petbottle.water",
                    "slot.diagram.petbottle.neck",
                    "slot.diagram.petbottle.rings1",
                    "slot.diagram.petbottle.rings2",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qno",
                prompt="",
                text="□ 12.",
                style_role="question",
                x=8.0,
                y=24.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qtext1",
                prompt="",
                text="유우병에 물을 가득 채운 후 페트병에 옮겨 담았습니다. 그림과 같이 물",
                style_role="question",
                x=52.0,
                y=24.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qtext2",
                prompt="",
                text="이 채워졌을 때 알맞은 말을 선택하세요.",
                style_role="question",
                x=12.0,
                y=62.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.label.yuubyeong",
                prompt="",
                text="유우병",
                style_role="label",
                x=312.0,
                y=146.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.label.petbottle",
                prompt="",
                text="페트병",
                style_role="label",
                x=460.0,
                y=270.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 유우병 , 페트병 )의 들이가 더 많습니다.",
                style_role="question",
                x=240.0,
                y=324.0,
                font_size=28,
            ),
            PathSlot(
                id="slot.diagram.yuubyeong.body",
                prompt="",
                d="M 414.0 84.0 C 404.0 84.0 394.0 92.0 392.0 102.0 L 385.0 132.0 C 383.0 142.0 388.0 151.0 397.0 155.0 L 424.0 166.0 C 435.0 170.0 447.0 165.0 451.0 154.0 L 457.0 138.0 C 460.0 128.0 457.0 117.0 448.0 111.0 L 425.0 86.0 C 422.0 84.0 418.0 84.0 414.0 84.0 Z",
            ),
            PathSlot(
                id="slot.diagram.yuubyeong.water",
                prompt="",
                d="M 389.0 114.0 L 444.0 139.0 L 435.0 151.0 L 381.0 126.0 Z",
            ),
            PathSlot(
                id="slot.diagram.yuubyeong.cap",
                prompt="",
                d="M 443.0 84.0 C 444.0 78.0 449.0 73.0 455.0 72.0 C 462.0 71.0 468.0 76.0 469.0 82.0 C 470.0 89.0 465.0 95.0 458.0 96.0 C 451.0 97.0 444.0 92.0 443.0 84.0 Z",
            ),
            PathSlot(
                id="slot.diagram.yuubyeong.spout",
                prompt="",
                d="M 466.0 84.0 C 472.0 86.0 477.0 91.0 480.0 98.0 C 483.0 104.0 483.0 112.0 480.0 118.0 L 469.0 109.0 C 472.0 104.0 472.0 98.0 470.0 93.0 C 469.0 90.0 467.0 87.0 466.0 84.0 Z",
            ),
            RectSlot(
                id="slot.diagram.petbottle.body",
                prompt="",
                x=438.0,
                y=112.0,
                width=48.0,
                height=116.0,
            ),
            RectSlot(
                id="slot.diagram.petbottle.water",
                prompt="",
                x=440.0,
                y=175.0,
                width=44.0,
                height=53.0,
            ),
            RectSlot(
                id="slot.diagram.petbottle.neck",
                prompt="",
                x=451.0,
                y=92.0,
                width=22.0,
                height=26.0,
            ),
            LineSlot(
                id="slot.diagram.petbottle.rings1",
                prompt="",
                x1=438.0,
                y1=126.0,
                x2=486.0,
                y2=126.0,
            ),
            LineSlot(
                id="slot.diagram.petbottle.rings2",
                prompt="",
                x1=438.0,
                y1=141.0,
                x2=486.0,
                y2=141.0,
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
