from __future__ import annotations

from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008680",
        title="원을 똑같이 둘로 나누는 선분 찾기",
        canvas=Canvas(width=940, height=343, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1",),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle",
                    "slot.seg.h",
                    "slot.seg.v",
                    "slot.center.dot",
                    "slot.label.center",
                    "slot.label.left",
                    "slot.label.right",
                    "slot.label.bottom",
                ),
            ),
            Region(
                id="region.choice",
                role="stem",
                flow="absolute",
                slot_ids=("slot.choice",),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=("slot.answer", "slot.explain"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 62. 원을 똑같이 둘로 나누는 선분을 찾아 기호를 선택하세요.",
                style_role="question",
                x=10.0,
                y=28.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle",
                prompt="",
                cx=479.0,
                cy=116.0,
                r=68.0,
                fill="none",
                stroke="#222222",
                stroke_width=1.8,
            ),
            LineSlot(
                id="slot.seg.h",
                prompt="",
                x1=411.0,
                y1=116.0,
                x2=547.0,
                y2=116.0,
                stroke="#333333",
                stroke_width=1.8,
            ),
            LineSlot(
                id="slot.seg.v",
                prompt="",
                x1=479.0,
                y1=116.0,
                x2=479.0,
                y2=184.0,
                stroke="#333333",
                stroke_width=1.8,
            ),
            CircleSlot(
                id="slot.center.dot",
                prompt="",
                cx=479.0,
                cy=116.0,
                r=3.2,
                fill="#d61f9d",
            ),
            TextSlot(
                id="slot.label.center",
                prompt="",
                text="ㅇ",
                style_role="diagram",
                x=473.0,
                y=108.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.label.left",
                prompt="",
                text="ㄱ",
                style_role="diagram",
                x=392.0,
                y=124.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.label.right",
                prompt="",
                text="ㄷ",
                style_role="diagram",
                x=551.0,
                y=124.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.label.bottom",
                prompt="",
                text="ㄴ",
                style_role="diagram",
                x=472.0,
                y=198.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="① 선분 ㅇㄱ      ② 선분 ㅇㄷ      ③ 선분 ㅇㄴ      ④ 선분 ㄱㄷ",
                style_role="question",
                x=86.0,
                y=228.0,
                font_size=40,
            ),
            TextSlot(
                id="slot.answer",
                prompt="",
                text="(정답) ④",
                style_role="question",
                x=10.0,
                y=278.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.explain",
                prompt="",
                text="(해설) 선분 ㄱㄷ이 원을 똑같이 둘로 나누는 선분입니다.",
                style_role="question",
                x=10.0,
                y=324.0,
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
    "problem_id": "S3_초등_3_008680",
    "problem_type": "choice_geometry_segment",
    "metadata": {
        "language": "ko",
        "question": "원을 똑같이 둘로 나누는 선분의 기호를 선택하는 문제",
        "instruction": "그림을 보고 알맞은 선분을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center", "type": "point", "label": "ㅇ"},
            {"id": "obj.point_g", "type": "point", "label": "ㄱ"},
            {"id": "obj.point_d", "type": "point", "label": "ㄷ"},
            {"id": "obj.point_n", "type": "point", "label": "ㄴ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.center", "obj.point_g", "obj.point_d", "obj.point_n"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.split_into_two_equal_parts"],
            },
            "plan": {
                "method": "diameter_identification",
                "description": "원을 중심을 지나 양끝이 원 위에 있는 선분이 원을 둘로 나누는지 확인한다.",
            },
            "execute": {
                "expected_operations": ["find_segment_through_center", "check_endpoints_on_circle", "select_symbol"]
            },
            "review": {"check_methods": ["geometry_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "segment_symbol", "description": "원을 똑같이 둘로 나누는 선분"},
        "value": "ㄱㄷ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008680",
    "problem_type": "choice_geometry_segment",
    "inputs": {
        "total_ticks": 0,
        "target_label": "원을 똑같이 둘로 나누는 선분",
        "target_ticks": 0,
        "target_count": 4,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": "원"},
        {"ref": "obj.center", "value": "중심 ㅇ"},
        {"ref": "obj.point_g", "value": "점 ㄱ"},
        {"ref": "obj.point_d", "value": "점 ㄷ"},
        {"ref": "obj.point_n", "value": "점 ㄴ"},
    ],
    "target": {"ref": "answer.target", "type": "segment_symbol"},
    "method": "diameter_identification",
    "plan": [
        "중심을 지나는 선분을 찾는다.",
        "선분의 양끝이 원 위의 점인지 확인한다.",
        "원을 똑같이 둘로 나누는 선분을 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "선분 ㄱㄷ은 중심 ㅇ을 지난다", "value": True},
        {"id": "step.2", "expr": "선분 ㄱㄷ의 양끝은 원 위의 점이다", "value": True},
        {"id": "step.3", "expr": "원을 똑같이 둘로 나누는 선분 선택", "value": "ㄱㄷ"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 선분이 원을 똑같이 둘로 나누는가",
            "expected": "ㄱㄷ",
            "actual": "ㄱㄷ",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "segment_symbol", "description": "원을 똑같이 둘로 나누는 선분"},
        "value": "ㄱㄷ",
        "unit": "",
    },
}
