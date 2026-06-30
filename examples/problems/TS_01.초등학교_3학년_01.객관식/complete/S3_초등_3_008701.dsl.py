from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, CircleSlot, LineSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008701",
        title="원의 지름을 모두 찾아 기호를 선택해 보세요.",
        canvas=Canvas(width=720, height=380, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q.text",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle.outline",
                    "slot.circle.center",
                    "slot.line.red",
                    "slot.line.orange",
                    "slot.line.green",
                    "slot.line.blue",
                    "slot.line.purple",
                    "slot.lb.giyeok",
                    "slot.lb.nieun",
                    "slot.lb.digeut",
                    "slot.lb.rieul",
                    "slot.lb.mieum",
                    "slot.lb.rieul.copy1",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="원의 지름을 모두 찾아 기호를 선택해 보세요.",
                style_role="question",
                x=85.0,
                y=32.0,
                font_size=28,
            ),
            CircleSlot(id="slot.circle.outline", prompt="", cx=370, cy=221, r=135, fill="none"),
            CircleSlot(id="slot.circle.center", prompt="", cx=370, cy=221, r=5, fill="#d32f2f"),
            LineSlot(id="slot.line.red", prompt="", x1=370, y1=221, x2=260, y2=141),
            LineSlot(id="slot.line.orange", prompt="", x1=372, y1=356, x2=367, y2=86),
            LineSlot(id="slot.line.green", prompt="", x1=303, y1=339, x2=438, y2=104),
            LineSlot(id="slot.line.blue", prompt="", x1=370, y1=221, x2=495, y2=171),
            LineSlot(id="slot.line.purple", prompt="", x1=235, y1=223, x2=505, y2=218),
            TextSlot(
                id="slot.lb.giyeok",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=235,
                y=141,
                font_size=30,
            ),
            TextSlot(
                id="slot.lb.nieun",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=345,
                y=75,
                font_size=30,
            ),
            TextSlot(
                id="slot.lb.digeut",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=571.0,
                y=45.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.rieul",
                prompt="",
                text="ㄹ",
                style_role="label",
                x=500,
                y=180,
                font_size=30,
            ),
            TextSlot(
                id="slot.lb.mieum",
                prompt="",
                text="ㅁ",
                style_role="label",
                x=515,
                y=230,
                font_size=30,
            ),
            TextSlot(
                id="slot.lb.rieul.copy1",
                prompt="",
                text="ㄷ",
                x=430,
                y=90,
                font_size=30,
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
    "problem_id": "S3_초등_3_008701",
    "problem_type": "geometry_circle_diameter_selection",
    "metadata": {
        "language": "ko",
        "question": "원의 지름을 모두 찾아 기호를 선택해 보세요.",
        "instruction": "원의 지름을 모두 찾아 기호를 선택해 보세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center", "type": "point", "role": "center"},
            {"id": "obj.chords", "type": "segments"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.center", "obj.chords"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.diameter_definition"],
            },
            "plan": {
                "method": "definition_check",
                "description": "중심을 지나고 원의 양쪽 경계를 잇는 선분인지 확인한다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_center_passing_segments",
                    "compare_endpoints_on_circle",
                    "select_matching_labels",
                ]
            },
            "review": {"check_methods": ["definition_match_check", "visual_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_labels", "description": "원의 지름에 해당하는 기호"},
        "value": 3,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008701",
    "problem_type": "geometry_circle_diameter_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "원의 지름에 해당하는 기호",
        "target_ticks": 0,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.center", "value": {"role": "center"}},
        {"ref": "obj.chords", "value": {"description": "여러 선분"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_labels"},
    "method": "definition_check",
    "plan": [
        "원의 중심을 지나는 선분을 찾습니다.",
        "원 위의 두 점을 잇는 선분인지 확인합니다.",
        "해당하는 기호를 선택합니다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "지름의 정의를 확인한다.",
            "value": "원의 중심을 지나면서 원 위의 두 점을 이은 선분",
        },
        {"id": "step.2", "expr": "도형에서 중심을 통과하는 선분을 확인한다.", "value": "확인됨"},
        {"id": "step.3", "expr": "해당 기호를 선택한다.", "value": "ㄴ, ㄷ, ㅁ"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선분이 중심을 지나는가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선분의 양 끝이 원 위에 있는가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_labels", "description": "원의 지름에 해당하는 기호"},
        "value": 3,
        "unit": "",
    },
}
