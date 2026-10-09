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
        id="S3_초등_3_008715",
        title="원에서 반지름을 나타내는 선분을 선택하시오",
        canvas=Canvas(width=960, height=360, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.inserted.freeform.1", "slot.inserted.circle.1"),
            ),
            Region(
                id="region.figure",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.seg_gs",
                    "slot.seg_nr",
                    "slot.seg_do",
                    "slot.seg_bm",
                    "slot.pt.o",
                    "slot.lb.g",
                    "slot.lb.s",
                    "slot.lb.n",
                    "slot.lb.r",
                    "slot.lb.d",
                    "slot.lb.m",
                    "slot.lb.b",
                    "slot.lb.m.copy1",
                ),
            ),
            Region(
                id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choices",)
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="원에서 반지름을 나타내는 선분을 선택하시오.",
                style_role="question",
                x=18.0,
                y=30.0,
                font_size=28,
            ),
            LineSlot(id="slot.seg_gs", prompt="", x1=235, y1=128, x2=345, y2=63),
            LineSlot(id="slot.seg_nr", prompt="", x1=230, y1=150, x2=310, y2=270),
            LineSlot(id="slot.seg_do", prompt="", x1=273, y1=256, x2=333, y2=166),
            LineSlot(id="slot.seg_bm", prompt="", x1=385, y1=76, x2=365, y2=266),
            CircleSlot(id="slot.pt.o", prompt="", cx=332, cy=167, r=3.5, fill="#d81b60"),
            TextSlot(
                id="slot.lb.g", prompt="", text="ㄱ", style_role="label", x=205, y=120, font_size=30
            ),
            TextSlot(
                id="slot.lb.s", prompt="", text="ㅅ", style_role="label", x=345, y=60, font_size=30
            ),
            TextSlot(
                id="slot.lb.n", prompt="", text="ㄴ", style_role="label", x=195, y=160, font_size=30
            ),
            TextSlot(
                id="slot.lb.r", prompt="", text="ㄹ", style_role="label", x=300, y=295, font_size=30
            ),
            TextSlot(
                id="slot.lb.d", prompt="", text="ㄷ", style_role="label", x=240, y=280, font_size=30
            ),
            TextSlot(
                id="slot.lb.m", prompt="", text="ㅁ", style_role="label", x=365, y=285, font_size=30
            ),
            TextSlot(
                id="slot.lb.b", prompt="", text="ㅂ", style_role="label", x=385, y=70, font_size=30
            ),
            TextSlot(
                id="slot.choices",
                prompt="",
                text="( 선분 ㄱㅅ , 선분 ㄴㄹ , 선분 ㄷㅇ , 선분 ㅂㅁ )",
                style_role="body",
                x=25,
                y=348,
                font_size=30,
            ),
            PathSlot(
                id="slot.inserted.freeform.1",
                prompt="",
                d="M 230.6666259765625 177.22222900390625 C 400.6666259765625 132.22222900390625 285.6666259765625 122.22222900390625",
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.inserted.circle.1",
                prompt="",
                cx=332,
                cy=167,
                r=105,
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.lb.m.copy1",
                prompt="",
                text="ㅇ",
                x=320,
                y=160,
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
    "problem_id": "S3_초등_3_008715",
    "problem_type": "geometry_circle_radius_choice",
    "metadata": {
        "language": "ko",
        "question": "원에서 반지름을 나타내는 선분을 선택하시오.",
        "instruction": "보기에서 반지름에 해당하는 선분을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center.o", "type": "point", "role": "center", "label": "ㅇ"},
            {"id": "obj.radius_candidate.d_o", "type": "segment", "label": "선분 ㄷㅇ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.center.o", "obj.radius_candidate.d_o"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.radius_definition"],
            },
            "plan": {
                "method": "definition_matching",
                "description": "원의 중심과 원 위의 한 점을 이은 선분을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_center",
                    "identify_point_on_circle",
                    "match_radius_definition",
                ]
            },
            "review": {"check_methods": ["definition_check", "candidate_comparison"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_segment", "description": "원의 반지름을 나타내는 선분"},
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008715",
    "problem_type": "geometry_circle_radius_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "선분 ㄷㅇ",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.center.o", "value": {"label": "ㅇ", "role": "center"}},
        {"ref": "obj.radius_candidate.d_o", "value": {"label": "선분 ㄷㅇ"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_segment"},
    "method": "definition_matching",
    "plan": [
        "원의 중심과 원 위의 한 점을 이은 선분을 찾는다.",
        "보기의 선분들 중 정의에 맞는 것을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "원의 중심과 원 위의 점을 잇는 선분 찾기", "value": "선분 ㄷㅇ"}
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선분 ㄷㅇ이 중심 ㅇ와 원 위의 점 ㄷ을 잇는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_segment", "description": "원의 반지름을 나타내는 선분"},
        "value": 1,
        "unit": "",
    },
}
