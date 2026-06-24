from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, LineSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008707",
        title="원의 반지름",
        canvas=Canvas(width=734.0, height=372.0, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle",
                    "slot.center1",
                    "slot.pt.da",
                    "slot.lbl.ga",
                    "slot.lbl.na",
                    "slot.lbl.da",
                    "slot.lbl.ra",
                    "slot.lbl.o",
                    "slot.seg.left",
                    "slot.seg.mid",
                    "slot.seg.diag",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.c1", "slot.c2", "slot.c3"),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="원의 반지름을 나타내는 선분의 기호를 선택해\n보세요.  ",
                style_role="question",
                x=140,
                y=35,
                font_size=30,
            ),
            CircleSlot(id="slot.center1", prompt="", cx=453, cy=175, r=5, fill="#ff4aa2"),
            CircleSlot(id="slot.circle", prompt="", cx=452, cy=176, r=110, fill="none"),
            LineSlot(id="slot.seg.left", prompt="", x1=370, y1=105, x2=370, y2=250),
            LineSlot(id="slot.seg.mid", prompt="", x1=455, y1=175, x2=560, y2=175),
            LineSlot(id="slot.seg.diag", prompt="", x1=425, y1=280, x2=560, y2=175),
            CircleSlot(
                id="slot.pt.da",
                prompt="",
                cx=390,
                cy=205,
                r=0,
                fill="#222222",
                stroke="#111111",
                stroke_width=2,
            ),
            TextSlot(
                id="slot.lbl.ga",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=335,
                y=105,
                font_size=30,
            ),
            TextSlot(
                id="slot.lbl.na",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=340,
                y=270,
                font_size=30,
            ),
            TextSlot(
                id="slot.lbl.da",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=405,
                y=310,
                font_size=30,
            ),
            TextSlot(
                id="slot.lbl.ra",
                prompt="",
                text="ㄹ",
                style_role="label",
                x=570,
                y=180,
                font_size=30,
            ),
            TextSlot(
                id="slot.lbl.o",
                prompt="",
                text="ㅇ",
                style_role="label",
                x=440,
                y=165,
                font_size=30,
            ),
            TextSlot(
                id="slot.c1",
                prompt="",
                text="① 선분 ㄱㄴ",
                style_role="choice",
                x=135,
                y=357,
                font_size=30,
            ),
            TextSlot(
                id="slot.c2",
                prompt="",
                text="② 선분 ㄷㄹ",
                style_role="choice",
                x=320,
                y=357,
                font_size=30,
            ),
            TextSlot(
                id="slot.c3",
                prompt="",
                text="③ 선분 ㅇㄹ",
                style_role="choice",
                x=505,
                y=357,
                font_size=30,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008707",
    "problem_type": "geometry_radius_multiple_choice",
    "metadata": {
        "language": "ko",
        "question": "원의 반지름을 나타내는 선분의 기호를 선택하는 문제",
        "instruction": "보기 중에서 반지름에 해당하는 선분을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center", "type": "point", "role": "center"},
            {"id": "obj.boundary_point", "type": "point", "role": "point_on_circle"},
            {"id": "obj.radius_segment", "type": "segment", "role": "radius"},
            {"id": "obj.options", "type": "choice_set"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.center", "obj.boundary_point", "obj.options"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.radius_definition", "rel.choose_correct_option"],
            },
            "plan": {
                "method": "definition_matching",
                "description": "원의 중심과 원 위의 한 점을 이은 선분이 반지름인지 확인한다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_center",
                    "identify_point_on_circle",
                    "match_segment_to_definition",
                ]
            },
            "review": {"check_methods": ["definition_check", "option_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "correct_choice", "description": "원의 반지름을 나타내는 선분의 기호"},
        "value": 3,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008707",
    "problem_type": "geometry_radius_multiple_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "원의 반지름을 나타내는 선분의 기호",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.center", "value": {"role": "center"}},
        {"ref": "obj.boundary_point", "value": {"role": "point_on_circle"}},
        {"ref": "obj.options", "value": {"count": 3}},
    ],
    "target": {"ref": "answer.target", "type": "correct_choice"},
    "method": "definition_matching",
    "plan": [
        "원의 중심에서 원 위의 한 점까지 이어진 선분이 반지름인지 확인한다.",
        "보기 중 그 정의에 맞는 선분의 기호를 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "원의 중심과 원 위의 한 점을 이은 선분을 찾기",
            "value": "선분 ㅇㄹ",
        },
        {"id": "step.2", "expr": "보기와 대응시키기", "value": 3},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "반지름 = 중심과 원 위의 한 점을 이은 선분",
            "expected": "선분 ㅇㄹ",
            "actual": "선분 ㅇㄹ",
            "pass": True,
        },
        {"id": "check.2", "expr": "선택지 번호 확인", "expected": 3, "actual": 3, "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "correct_choice", "description": "원의 반지름을 나타내는 선분의 기호"},
        "value": 3,
        "unit": "",
    },
}
