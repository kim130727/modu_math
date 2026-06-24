from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, CircleSlot, LineSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008748",
        title="물병의 들이 비교",
        canvas=Canvas(width=960, height=460, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.qnum",
                    "slot.q1",
                    "slot.q2",
                    "slot.bottle.top",
                    "slot.bottle.bottom",
                    "slot.choice",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="45.",
                style_role="question",
                x=18.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q1",
                prompt="",
                text="ㄱ 물병에 물을 가득 채운 후 ㄴ 물병에 옮겨 담았습니다. 그림과 같이",
                style_role="question",
                x=90.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="물을 채웠을 때 들이가 더 많은 물병을 선택해 보세요.",
                style_role="question",
                x=18.0,
                y=68.0,
                font_size=28,
            ),
            RectSlot(id="slot.bottle.top", prompt="", x=430.0, y=85.0, width=150.0, height=95.0),
            RectSlot(
                id="slot.bottle.bottom", prompt="", x=490.0, y=120.0, width=82.0, height=150.0
            ),
            CircleSlot(
                id="slot.bottle.top.label", prompt="", cx=482.0, cy=114.0, r=13.0, fill="#FFFFFF"
            ),
            CircleSlot(
                id="slot.bottle.bottom.label", prompt="", cx=531.0, cy=195.0, r=13.0, fill="#FFFFFF"
            ),
            TextSlot(
                id="slot.bottle.top.text",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=475.0,
                y=122.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.bottle.bottom.text",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=524.0,
                y=203.0,
                font_size=22,
            ),
            LineSlot(id="slot.bottle.top.neck1", prompt="", x1=503.0, y1=103.0, x2=515.0, y2=116.0),
            LineSlot(id="slot.bottle.top.neck2", prompt="", x1=515.0, y1=116.0, x2=517.0, y2=133.0),
            LineSlot(
                id="slot.bottle.bottom.neck1", prompt="", x1=519.0, y1=122.0, x2=519.0, y2=137.0
            ),
            LineSlot(
                id="slot.bottle.bottom.neck2", prompt="", x1=519.0, y1=137.0, x2=505.0, y2=146.0
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( ㄱ 물병, ㄴ 물병 )",
                style_role="choice",
                x=690.0,
                y=292.0,
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
    "problem_id": "S3_초등_3_008748",
    "problem_type": "comparison_capacity_selection",
    "metadata": {
        "language": "ko",
        "question": "그림을 보고 더 많은 물이 들어가는 물병을 고르는 문제",
        "instruction": "더 많은 들이의 물병을 선택하시오.",
    },
    "domain": {
        "objects": [
            {"id": "obj.bottle_a", "type": "bottle", "label": "ㄱ"},
            {"id": "obj.bottle_b", "type": "bottle", "label": "ㄴ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.bottle_a", "obj.bottle_b", "rel.pour_a_to_b"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_capacity"],
            },
            "plan": {
                "method": "visual_comparison",
                "description": "물의 이동 후 상태를 보고 더 많은 들이의 병을 고른다.",
            },
            "execute": {
                "expected_operations": ["compare_filled_state", "identify_not_full_container"]
            },
            "review": {"check_methods": ["answer_matches_explanation"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "더 많은 들이의 물병"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008748",
    "problem_type": "comparison_capacity_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "ㄴ 물병",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.bottle_a", "value": {"label": "ㄱ"}},
        {"ref": "obj.bottle_b", "value": {"label": "ㄴ"}},
    ],
    "target": {"ref": "answer.target", "type": "choice"},
    "method": "visual_comparison",
    "plan": [
        "그림에서 ㄱ 물병의 물이 ㄴ 물병에 옮겨 담긴 상태를 확인한다.",
        "ㄴ 물병이 가득 차지 않았는지 살펴 더 큰 들이의 병을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "ㄱ 물병의 물을 ㄴ 물병에 옮겨 담은 상태를 확인",
            "value": "ㄴ 물병이 가득 차지 않음",
        },
        {"id": "step.2", "expr": "더 많은 들이의 물병 선택", "value": "ㄴ 물병"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "해설과 선택이 일치하는가",
            "expected": "ㄴ 물병",
            "actual": "ㄴ 물병",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "더 많은 들이의 물병"},
        "value": 0,
        "unit": "",
    },
}
