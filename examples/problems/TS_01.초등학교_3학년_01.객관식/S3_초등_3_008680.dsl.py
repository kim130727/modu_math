from __future__ import annotations

from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008680",
        title="원을 똑같이 둘로 나누는 선분 찾기",
        canvas=Canvas(width=900, height=343, coordinate_mode="logical"),
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
                slot_ids=( ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text = '원을 똑같이 둘로 나누는 선분을 찾아 기호를 선택하세요.', style_role="question",
                x=10.0,
                y=28.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle",
                prompt="",
                cx = 380, cy = 146, r = 85, fill="none",
                stroke="#222222",
                stroke_width=1.8,
            ),
            LineSlot(
                id="slot.seg.h",
                prompt="",
                x1 = 295, y1 = 145, x2 = 465, y2 = 145, stroke="#333333",
                stroke_width=1.8,
            ),
            LineSlot(
                id="slot.seg.v",
                prompt="",
                x1 = 380, y1 = 145, x2 = 380, y2 = 230, stroke="#333333",
                stroke_width=1.8,
            ),
            CircleSlot(
                id="slot.center.dot",
                prompt="",
                cx = 380, cy = 145, r = 5, fill="#d61f9d",
            ),
            TextSlot(
                id="slot.label.center",
                prompt="",
                text = 'ㅇ', style_role="diagram",
                x = 385, y = 130, font_size = 25),
            TextSlot(
                id="slot.label.left",
                prompt="",
                text = 'ㄱ', style_role="diagram",
                x = 260, y = 160, font_size = 25),
            TextSlot(
                id="slot.label.right",
                prompt="",
                text = 'ㄷ', style_role="diagram",
                x = 480, y = 160, font_size = 25),
            TextSlot(
                id="slot.label.bottom",
                prompt="",
                text = 'ㄴ', style_role="diagram",
                x = 385, y = 255, font_size = 25),
            TextSlot(
                id="slot.choice",
                prompt="",
                text = '① 선분 ㅇㄱ      ② 선분 ㅇㄷ      ③ 선분 ㅇㄴ      ④ 선분 ㄱㄷ', style_role="question",
                x = 35, y = 295, font_size = 28, fill = '#111111'),
            
            
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
