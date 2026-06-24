from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    LineSlot,
    PolygonSlot,
    PathSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008815",
        title="들이가 더 많은 그릇 고르기",
        canvas=Canvas(width=940, height=562, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.box", "slot.num", "slot.q1", "slot.q2", "slot.q3"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.top.a1",
                    "slot.top.a2",
                    "slot.top.a3",
                    "slot.top.a4",
                    "slot.top.a5",
                    "slot.top.a6",
                    "slot.top.b1",
                    "slot.top.b2",
                    "slot.top.b3",
                    "slot.top.b4",
                    "slot.top.b5",
                    "slot.top.b6",
                    "slot.top.la",
                    "slot.top.lb",
                    "slot.choice",
                    "slot.bot.a1",
                    "slot.bot.a2",
                    "slot.bot.a3",
                    "slot.bot.a4",
                    "slot.bot.a5",
                    "slot.bot.a6",
                    "slot.bot.b1",
                    "slot.bot.b2",
                    "slot.bot.b3",
                    "slot.bot.b4",
                    "slot.bot.b5",
                    "slot.bot.b6",
                    "slot.bot.la",
                    "slot.bot.lb",
                ),
            ),
        ),
        slots=(
            RectSlot(id="slot.box", prompt="", x=11.0, y=8.0, width=14.0, height=14.0),
            TextSlot(
                id="slot.num",
                prompt="",
                text="48.",
                style_role="question",
                x=33.0,
                y=21.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q1",
                prompt="",
                text="가 그릇과 나 그릇에 물을 가득 채운 후 모양과 크기가 같은 그릇에 옮겨",
                style_role="question",
                x=46.0,
                y=20.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="담았더니 그림과 같이 물이 채워졌습니다. 들이가 더 많은 그릇을 선택해",
                style_role="question",
                x=28.0,
                y=55.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="보세요.",
                style_role="question",
                x=28.0,
                y=90.0,
                font_size=28,
            ),
            CircleSlot(id="slot.top.la", prompt="", cx=292.0, cy=126.0, r=11.0, fill="#FFFFFF"),
            TextSlot(
                id="slot.top.lb",
                prompt="",
                text="가",
                style_role="label",
                x=284.0,
                y=132.0,
                font_size=24,
            ),
            PathSlot(
                id="slot.top.a1",
                prompt="",
                d="M 342.0 120.0 C 332.0 130.0 326.0 145.0 326.0 162.0 C 326.0 189.0 346.0 209.0 367.0 209.0 C 388.0 209.0 408.0 189.0 408.0 162.0 C 408.0 145.0 402.0 130.0 392.0 120.0",
            ),
            PathSlot(
                id="slot.top.a2", prompt="", d="M 346.0 119.0 C 353.0 113.0 381.0 113.0 388.0 119.0"
            ),
            PathSlot(
                id="slot.top.a3", prompt="", d="M 341.0 120.0 C 352.0 128.0 381.0 128.0 393.0 120.0"
            ),
            PathSlot(
                id="slot.top.a4", prompt="", d="M 330.0 160.0 C 344.0 170.0 390.0 170.0 406.0 160.0"
            ),
            PathSlot(
                id="slot.top.a5", prompt="", d="M 337.0 160.0 C 349.0 198.0 384.0 198.0 398.0 160.0"
            ),
            PathSlot(
                id="slot.top.a6", prompt="", d="M 342.0 123.0 C 341.0 145.0 342.0 167.0 367.0 209.0"
            ),
            CircleSlot(id="slot.top.b1", prompt="", cx=409.0, cy=134.0, r=4.0, fill="#FFFFFF"),
            PathSlot(
                id="slot.top.b2",
                prompt="",
                d="M 479.0 120.0 C 469.0 130.0 463.0 145.0 463.0 162.0 C 463.0 189.0 483.0 209.0 504.0 209.0 C 525.0 209.0 545.0 189.0 545.0 162.0 C 545.0 145.0 539.0 130.0 529.0 120.0",
            ),
            PathSlot(
                id="slot.top.b3", prompt="", d="M 483.0 119.0 C 490.0 113.0 518.0 113.0 525.0 119.0"
            ),
            PathSlot(
                id="slot.top.b4", prompt="", d="M 478.0 120.0 C 489.0 128.0 518.0 128.0 530.0 120.0"
            ),
            PathSlot(
                id="slot.top.b5", prompt="", d="M 467.0 160.0 C 481.0 170.0 527.0 170.0 543.0 160.0"
            ),
            PathSlot(
                id="slot.top.b6", prompt="", d="M 474.0 160.0 C 486.0 188.0 521.0 188.0 535.0 160.0"
            ),
            CircleSlot(id="slot.top.lb", prompt="", cx=544.0, cy=126.0, r=11.0, fill="#FFFFFF"),
            TextSlot(
                id="slot.top.la",
                prompt="",
                text="나",
                style_role="label",
                x=535.0,
                y=132.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 가 , 나 ) 그릇",
                style_role="question",
                x=748.0,
                y=294.0,
                font_size=28,
            ),
            CircleSlot(id="slot.bot.la", prompt="", cx=44.0, cy=399.0, r=11.0, fill="#FFFFFF"),
            TextSlot(
                id="slot.bot.lb",
                prompt="",
                text="가",
                style_role="label",
                x=35.0,
                y=405.0,
                font_size=24,
            ),
            PathSlot(
                id="slot.bot.a1",
                prompt="",
                d="M 94.0 387.0 C 84.0 397.0 78.0 412.0 78.0 429.0 C 78.0 456.0 98.0 476.0 119.0 476.0 C 140.0 476.0 160.0 456.0 160.0 429.0 C 160.0 412.0 154.0 397.0 144.0 387.0",
            ),
            PathSlot(
                id="slot.bot.a2", prompt="", d="M 98.0 386.0 C 105.0 380.0 133.0 380.0 140.0 386.0"
            ),
            PathSlot(
                id="slot.bot.a3", prompt="", d="M 93.0 387.0 C 104.0 395.0 133.0 395.0 145.0 387.0"
            ),
            PathSlot(
                id="slot.bot.a4", prompt="", d="M 82.0 427.0 C 96.0 437.0 142.0 437.0 158.0 427.0"
            ),
            PathSlot(
                id="slot.bot.a5", prompt="", d="M 89.0 427.0 C 101.0 465.0 136.0 465.0 150.0 427.0"
            ),
            PathSlot(
                id="slot.bot.a6", prompt="", d="M 94.0 390.0 C 93.0 412.0 94.0 434.0 119.0 476.0"
            ),
            CircleSlot(id="slot.bot.b1", prompt="", cx=161.0, cy=401.0, r=4.0, fill="#FFFFFF"),
            PathSlot(
                id="slot.bot.b2",
                prompt="",
                d="M 232.0 387.0 C 222.0 397.0 216.0 412.0 216.0 429.0 C 216.0 456.0 236.0 476.0 257.0 476.0 C 278.0 476.0 298.0 456.0 298.0 429.0 C 298.0 412.0 292.0 397.0 282.0 387.0",
            ),
            PathSlot(
                id="slot.bot.b3", prompt="", d="M 236.0 386.0 C 243.0 380.0 271.0 380.0 278.0 386.0"
            ),
            PathSlot(
                id="slot.bot.b4", prompt="", d="M 231.0 387.0 C 242.0 395.0 271.0 395.0 283.0 387.0"
            ),
            PathSlot(
                id="slot.bot.b5", prompt="", d="M 220.0 427.0 C 234.0 437.0 280.0 437.0 296.0 427.0"
            ),
            PathSlot(
                id="slot.bot.b6", prompt="", d="M 227.0 427.0 C 239.0 455.0 274.0 455.0 288.0 427.0"
            ),
            CircleSlot(id="slot.bot.lb", prompt="", cx=297.0, cy=399.0, r=11.0, fill="#FFFFFF"),
            TextSlot(
                id="slot.bot.la",
                prompt="",
                text="나",
                style_role="label",
                x=288.0,
                y=405.0,
                font_size=24,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008815",
    "problem_type": "comparison_selection",
    "metadata": {
        "language": "ko",
        "question": "가 그릇과 나 그릇을 비교하여 들이가 더 많은 그릇을 고르는 문제",
        "instruction": "들이가 더 많은 그릇을 선택한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.container.ga", "type": "container", "label": "가"},
            {"id": "obj.container.na", "type": "container", "label": "나"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.container.ga", "obj.container.na", "rel.compare_capacity"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_capacity"],
            },
            "plan": {
                "method": "visual_comparison",
                "description": "그림에 보이는 물 높이를 비교하여 들이가 더 많은 그릇을 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_visual_fill_levels",
                    "select_container_with_more_capacity",
                ]
            },
            "review": {"check_methods": ["match_with_visible_explanation"]},
        },
    },
    "answer": {
        "target": {"type": "selected_container", "description": "들이가 더 많은 그릇"},
        "value": 1,
        "unit": "",
    },
}
SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008815",
    "problem_type": "comparison_selection",
    "inputs": {
        "total_ticks": 2,
        "target_label": "들이가 더 많은 그릇",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.container.ga", "value": {"label": "가"}},
        {"ref": "obj.container.na", "value": {"label": "나"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_container"},
    "plan": ["그림에서 두 그릇의 물 높이를 비교한다.", "더 많이 차 있는 그릇을 선택한다."],
    "method": "visual_comparison",
    "steps": [
        {
            "id": "step.1",
            "expr": "가 그릇의 물 높이와 나 그릇의 물 높이를 비교한다.",
            "value": "가가 더 높게 보임",
        },
        {"id": "step.2", "expr": "더 많이 차 있는 그릇을 선택한다.", "value": "가"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "해설 문장과 선택 결과가 일치하는지 확인한다.",
            "expected": "가",
            "actual": "가",
            "pass": True,
        }
    ],
    "answer": {"value": 1, "unit": "", "derived_from": "step.2"},
}
