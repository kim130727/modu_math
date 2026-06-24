from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_009009",
        title="반직선 고르기",
        canvas=Canvas(width=852, height=324, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.no", "slot.q.text"),
            ),
            Region(
                id="region.options",
                role="body",
                flow="absolute",
                slot_ids=(
                    "slot.opt1.line",
                    "slot.opt1.pt.left",
                    "slot.opt1.pt.right",
                    "slot.opt1.lb.left",
                    "slot.opt1.lb.right",
                    "slot.opt2.line",
                    "slot.opt2.pt.left",
                    "slot.opt2.pt.right",
                    "slot.opt2.lb.left",
                    "slot.opt2.lb.right",
                ),
            ),
            Region(
                id="region.answer", role="answer", flow="absolute", slot_ids=("slot.answer.line",)
            ),
            Region(id="region.explanation", role="explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q.no",
                prompt="",
                text="□ 48.",
                style_role="question",
                x=10.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="점 ㄱ에서 시작하여 점 ㄴ을 지나 오른쪽으로 길게 늘인 곧은 선을 선택하세요.",
                style_role="question",
                x=64.0,
                y=26.0,
                font_size=28,
            ),
            LineSlot(id="slot.opt1.line", prompt="", x1=306.0, y1=98.0, x2=561.0, y2=98.0),
            CircleSlot(id="slot.opt1.pt.left", prompt="", cx=304.0, cy=98.0, r=4.0, fill="#222222"),
            CircleSlot(
                id="slot.opt1.pt.right", prompt="", cx=512.0, cy=98.0, r=4.0, fill="#222222"
            ),
            TextSlot(
                id="slot.opt1.lb.left",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=296.0,
                y=76.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt1.lb.right",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=505.0,
                y=76.0,
                font_size=28,
            ),
            LineSlot(id="slot.opt2.line", prompt="", x1=304.0, y1=143.0, x2=560.0, y2=143.0),
            CircleSlot(
                id="slot.opt2.pt.left", prompt="", cx=304.0, cy=143.0, r=4.0, fill="#222222"
            ),
            CircleSlot(
                id="slot.opt2.pt.right", prompt="", cx=559.0, cy=143.0, r=4.0, fill="#222222"
            ),
            TextSlot(
                id="slot.opt2.lb.left",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=296.0,
                y=120.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt2.lb.right",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=553.0,
                y=120.0,
                font_size=28,
            ),
            LineSlot(id="slot.answer.line", prompt="", x1=67.0, y1=215.0, x2=232.0, y2=215.0),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_009009",
    "problem_type": "선의 종류",
    "metadata": {
        "language": "ko",
        "question": "점 ㄱ에서 시작하여 점 ㄴ을 지나 오른쪽으로 길게 늘인 곧은 선을 선택하세요.",
        "instruction": "보기에서 알맞은 선을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.point_giyeok", "type": "point", "name": "ㄱ"},
            {"id": "obj.point_nieun", "type": "point", "name": "ㄴ"},
            {"id": "obj.line_candidate_1", "type": "line_candidate"},
            {"id": "obj.line_candidate_2", "type": "line_candidate"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.point_giyeok", "obj.point_nieun"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.starts_at", "rel.passes_through", "rel.direction_right"],
            },
            "plan": {
                "method": "shape_matching",
                "description": "시작점, 지나가는 점, 진행 방향을 보고 알맞은 선의 모양을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_start_point",
                    "identify_pass_through_point",
                    "compare_direction",
                ]
            },
            "review": {"check_methods": ["condition_matching", "direction_consistency"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "반직선",
            "description": "점 ㄱ에서 시작하여 점 ㄴ을 지나 오른쪽으로 길게 늘인 곧은 선",
        },
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009009",
    "problem_type": "선의 종류",
    "inputs": {
        "total_ticks": 0,
        "target_label": "반직선",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.point_giyeok", "value": "ㄱ"},
        {"ref": "obj.point_nieun", "value": "ㄴ"},
        {"ref": "rel.starts_at", "value": "점 ㄱ에서 시작"},
        {"ref": "rel.passes_through", "value": "점 ㄴ을 지남"},
        {"ref": "rel.direction_right", "value": "오른쪽으로 길게 늘어남"},
    ],
    "target": {"ref": "answer.target", "type": "반직선"},
    "method": "shape_matching",
    "plan": ["시작점과 지나가는 점, 방향을 확인한다.", "조건에 맞는 선의 종류를 고른다."],
    "steps": [
        {"id": "step.1", "expr": "시작점 = ㄱ", "value": "ㄱ"},
        {"id": "step.2", "expr": "지나는 점 = ㄴ", "value": "ㄴ"},
        {"id": "step.3", "expr": "방향 = 오른쪽", "value": "오른쪽"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "시작점이 ㄱ인지 확인",
            "expected": "ㄱ",
            "actual": "ㄱ",
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "ㄴ을 지나는지 확인",
            "expected": "ㄴ",
            "actual": "ㄴ",
            "pass": True,
        },
        {
            "id": "check.3",
            "expr": "오른쪽으로 길게 늘어나는지 확인",
            "expected": "오른쪽",
            "actual": "오른쪽",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "반직선",
            "description": "점 ㄱ에서 시작하여 점 ㄴ을 지나 오른쪽으로 길게 늘인 곧은 선",
        },
        "value": 0,
        "unit": "",
    },
}
