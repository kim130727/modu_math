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
        id="S3_초등_3_009049",
        title="직선을 알아보고",
        canvas=Canvas(width=840.0, height=470.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.num", "slot.stem.1", "slot.stem.2"),
            ),
            Region(
                id="region.demo_box",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.box.demo",
                    "slot.demo.left.arrow",
                    "slot.demo.left.text",
                    "slot.demo.left.p1",
                    "slot.demo.left.p2",
                    "slot.demo.right.arrow",
                    "slot.demo.right.text",
                    "slot.demo.right.p1",
                    "slot.demo.right.p2",
                    "slot.teacher",
                    "slot.speech.bubble",
                    "slot.speech.text.1",
                    "slot.speech.text.2",
                    "slot.speech.text.3",
                ),
            ),
            Region(
                id="region.choice",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.choice.left.p1",
                    "slot.choice.left.p2",
                    "slot.choice.left.line",
                    "slot.choice.left.lb1",
                    "slot.choice.left.lb2",
                    "slot.choice.right.p1",
                    "slot.choice.right.p2",
                    "slot.choice.right.line",
                    "slot.choice.right.lb1",
                    "slot.choice.right.lb2",
                    "slot.answer.line",
                ),
            ),
            Region(id="region.footer", role="explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.num",
                prompt="",
                text="87.",
                style_role="question",
                x=41.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.stem.1",
                prompt="",
                text="직선을 알아보고자 합니다. 점 ㄱ과 점 ㄴ을 지나 양쪽으로 길게 늘인 곧",
                style_role="question",
                x=82.0,
                y=24.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.stem.2",
                prompt="",
                text="은 선을 선택해 보세요.",
                style_role="question",
                x=82.0,
                y=58.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.box.demo",
                prompt="",
                x=91.0,
                y=86.0,
                width=411.0,
                height=94.0,
                rx=10.0,
                ry=10.0,
                fill="none",
                stroke="#EA8AC8",
                stroke_width=2.0,
            ),
            PathSlot(
                id="slot.demo.left.arrow",
                prompt="",
                d="M 109.0 138.0 L 121.0 126.0 L 121.0 132.0 L 184.0 132.0 L 184.0 144.0 L 121.0 144.0 L 121.0 150.0 Z",
                fill="none",
                stroke="#FF9ACD",
                stroke_width=1.8,
            ),
            TextSlot(
                id="slot.demo.left.text",
                prompt="",
                text="점 ㄱ을 지나 끝없이 늘어난다.",
                style_role="label",
                x=119.0,
                y=139.0,
                font_size=20,
            ),
            CircleSlot(
                id="slot.demo.left.p1", prompt="", cx=102.0, cy=139.0, r=2.8, fill="#222222"
            ),
            CircleSlot(
                id="slot.demo.left.p2", prompt="", cx=251.0, cy=139.0, r=2.8, fill="#222222"
            ),
            PathSlot(
                id="slot.demo.right.arrow",
                prompt="",
                d="M 352.0 138.0 L 340.0 126.0 L 340.0 132.0 L 279.0 132.0 L 279.0 144.0 L 340.0 144.0 L 340.0 150.0 Z",
                fill="none",
                stroke="#FF9ACD",
                stroke_width=1.8,
            ),
            TextSlot(
                id="slot.demo.right.text",
                prompt="",
                text="점 ㄴ을 지나 끝없이 늘어난다.",
                style_role="label",
                x=291.0,
                y=139.0,
                font_size=20,
            ),
            CircleSlot(
                id="slot.demo.right.p1", prompt="", cx=364.0, cy=139.0, r=2.8, fill="#222222"
            ),
            CircleSlot(
                id="slot.demo.right.p2", prompt="", cx=219.0, cy=139.0, r=2.8, fill="#222222"
            ),
            PathSlot(
                id="slot.teacher",
                prompt="",
                d="M 540.0 120.0 C 543.0 102.0, 561.0 93.0, 577.0 93.0 C 592.0 93.0, 608.0 101.0, 611.0 118.0 C 616.0 145.0, 599.0 168.0, 575.0 171.0 C 549.0 169.0, 533.0 145.0, 540.0 120.0 Z",
                fill="#5A3C2E",
                stroke="none",
            ),
            PathSlot(
                id="slot.speech.bubble",
                prompt="",
                d="M 615.0 95.0 C 652.0 82.0, 718.0 82.0, 748.0 95.0 C 770.0 106.0, 772.0 149.0, 748.0 163.0 C 716.0 182.0, 650.0 182.0, 618.0 164.0 C 609.0 159.0, 603.0 152.0, 602.0 143.0 C 600.0 136.0, 603.0 128.0, 609.0 122.0 C 602.0 112.0, 604.0 101.0, 615.0 95.0 Z",
                fill="none",
                stroke="#666666",
                stroke_width=1.8,
            ),
            TextSlot(
                id="slot.speech.text.1",
                prompt="",
                text="선분을 양쪽으로",
                style_role="label",
                x=635.0,
                y=109.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.speech.text.2",
                prompt="",
                text="끝없이 늘인 곧은 선을",
                style_role="label",
                x=624.0,
                y=135.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.speech.text.3",
                prompt="",
                text="직선이라고 한다닷.",
                style_role="label",
                x=631.0,
                y=161.0,
                font_size=22,
            ),
            LineSlot(
                id="slot.choice.left.line",
                prompt="",
                x1=166.0,
                y1=228.0,
                x2=337.0,
                y2=228.0,
                stroke="#444444",
                stroke_width=2.0,
            ),
            CircleSlot(
                id="slot.choice.left.p1", prompt="", cx=162.0, cy=228.0, r=2.8, fill="#222222"
            ),
            CircleSlot(
                id="slot.choice.left.p2", prompt="", cx=339.0, cy=228.0, r=2.8, fill="#222222"
            ),
            TextSlot(
                id="slot.choice.left.lb1",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=158.0,
                y=214.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.choice.left.lb2",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=333.0,
                y=214.0,
                font_size=22,
            ),
            LineSlot(
                id="slot.choice.right.line",
                prompt="",
                x1=505.0,
                y1=228.0,
                x2=679.0,
                y2=228.0,
                stroke="#444444",
                stroke_width=2.0,
            ),
            CircleSlot(
                id="slot.choice.right.p1", prompt="", cx=500.0, cy=228.0, r=2.8, fill="#222222"
            ),
            CircleSlot(
                id="slot.choice.right.p2", prompt="", cx=681.0, cy=228.0, r=2.8, fill="#222222"
            ),
            TextSlot(
                id="slot.choice.right.lb1",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=495.0,
                y=214.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.choice.right.lb2",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=675.0,
                y=214.0,
                font_size=22,
            ),
            LineSlot(
                id="slot.answer.line",
                prompt="",
                x1=64.0,
                y1=325.0,
                x2=272.0,
                y2=325.0,
                stroke="#444444",
                stroke_width=2.0,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_009049",
    "problem_type": "개념_판별",
    "metadata": {
        "language": "ko",
        "question": "직선을 알아보고 점 ㄱ과 점 ㄴ을 지나 양쪽으로 길게 늘인 곧은 선을 선택하는 문제",
        "instruction": "보이는 구성만 기록한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.point_g", "type": "point", "label": "ㄱ"},
            {"id": "obj.point_n", "type": "point", "label": "ㄴ"},
            {"id": "obj.line_segment_example", "type": "line_segment_example"},
            {"id": "obj.line_example", "type": "line_example"},
            {"id": "obj.answer_blank", "type": "answer_blank"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.point_g",
                    "obj.point_n",
                    "obj.line_segment_example",
                    "obj.line_example",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.define_line", "rel.extend_both_directions"],
            },
            "plan": {"method": "개념_확인", "description": "직선의 정의와 예시 구성을 확인한다."},
            "execute": {"expected_operations": ["identify_defined_term", "compare_examples"]},
            "review": {"check_methods": ["definition_match", "visual_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "concept_selection",
            "description": "점 ㄱ과 점 ㄴ을 지나 양쪽으로 길게 늘인 곧은 선",
        },
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009049",
    "problem_type": "개념_판별",
    "inputs": {
        "total_ticks": 0,
        "target_label": "직선",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.point_g", "value": {"label": "ㄱ"}},
        {"ref": "obj.point_n", "value": {"label": "ㄴ"}},
    ],
    "target": {"ref": "answer.target", "type": "concept_selection"},
    "method": "개념_확인",
    "plan": [
        "그림과 문장을 보고 직선의 정의를 확인한다.",
        "보이는 구성만 기록하고 정답은 추론하지 않는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "점 ㄱ과 점 ㄴ을 지난다", "value": "definition_condition"},
        {"id": "step.2", "expr": "양쪽으로 길게 늘인 곧은 선", "value": "line"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "문장에 직선의 정의가 포함되는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "concept_selection",
            "description": "점 ㄱ과 점 ㄴ을 지나 양쪽으로 길게 늘인 곧은 선",
        },
        "value": 0,
        "unit": "",
    },
}
