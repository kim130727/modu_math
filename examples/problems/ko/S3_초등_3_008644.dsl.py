from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    # 원의 중심 C=(380, 190), 반지름 R=90
    stem_slots = (
        TextSlot(
            id="slot.question.line1",
            text="점 ㅇ는 원의 중심입니다. 원의 반지름은 어느 선분인지 모두 선택해 보세요.",
            style_role="question",
            x=40,
            y=50,
            font_size=25,
        ),
    )

    diagram_slots = (
        CircleSlot(
            id="slot.figure.circle",
            cx=380,
            cy=190,
            r=90,
            fill="none",
            stroke="#333333",
            stroke_width=1.5,
        ),
        # 점 ㄱ(328.4, 116.3) ~ 점 ㅅ(431.6, 116.3) [선분 ㄱㅅ - 가]
        LineSlot(
            id="slot.segment.ga",
            x1=328.4,
            y1=116.3,
            x2=431.6,
            y2=116.3,
            stroke="#333333",
            stroke_width=1.5,
        ),
        # 점 ㄴ(298.4, 152.0) ~ 점 ㅅ(431.6, 116.3) [선분 ㄴㅅ - 바]
        LineSlot(
            id="slot.segment.na_to_sa",
            x1=298.4,
            y1=152.0,
            x2=431.6,
            y2=116.3,
            stroke="#333333",
            stroke_width=1.5,
        ),
        # 점 ㄹ(425.0, 267.9) ~ 점 ㅂ(464.6, 159.2) [선분 ㄹㅂ - 마]
        LineSlot(
            id="slot.segment.la_ba",
            x1=425.0,
            y1=267.9,
            x2=464.6,
            y2=159.2,
            stroke="#333333",
            stroke_width=1.5,
        ),
        # 중심 ㅇ(380, 190) ~ 점 ㄴ(298.4, 152.0) [선분 ㅇㄴ - 나 (반지름)]
        LineSlot(
            id="slot.segment.o_na",
            x1=380.0,
            y1=190.0,
            x2=298.4,
            y2=152.0,
            stroke="#333333",
            stroke_width=1.5,
        ),
        # 중심 ㅇ(380, 190) ~ 점 ㄷ(328.4, 263.7) [선분 ㅇㄷ - 다 (반지름)]
        LineSlot(
            id="slot.segment.o_da",
            x1=380.0,
            y1=190.0,
            x2=328.4,
            y2=263.7,
            stroke="#333333",
            stroke_width=1.5,
        ),
        # 중심 ㅇ(380, 190) ~ 점 ㅁ(470.0, 190.0) [선분 ㅇㅁ - 라 (반지름)]
        LineSlot(
            id="slot.segment.o_ma",
            x1=380.0,
            y1=190.0,
            x2=470.0,
            y2=190.0,
            stroke="#333333",
            stroke_width=1.5,
        ),
        # 중심점 dot
        CircleSlot(
            id="slot.center.dot",
            cx=380,
            cy=190,
            r=5,
            fill="#ec2aa0",
            stroke="#ec2aa0",
            stroke_width=1,
        ),
        # 점 라벨들
        TextSlot(id="slot.label.giyeok", text="ㄱ", style_role="label", x=315, y=105, font_size=20),
        TextSlot(id="slot.label.siot", text="ㅅ", style_role="label", x=440, y=110, font_size=20),
        TextSlot(id="slot.label.bieup", text="ㅂ", style_role="label", x=475, y=155, font_size=20),
        TextSlot(id="slot.label.nieun", text="ㄴ", style_role="label", x=275, y=155, font_size=20),
        TextSlot(id="slot.label.mieum", text="ㅁ", style_role="label", x=480, y=196, font_size=20),
        TextSlot(id="slot.label.digeut", text="ㄷ", style_role="label", x=310, y=285, font_size=20),
        TextSlot(id="slot.label.rieul", text="ㄹ", style_role="label", x=428, y=290, font_size=20, fill="#111111"),
        TextSlot(id="slot.label.ieung", text="ㅇ", style_role="label", x=382, y=215, font_size=20, fill="#111111"),
    )

    choice_slots = (
        TextSlot(id="slot.choice.ga", text="㉮ 선분 ㄱㅅ", style_role="choice", x=90, y=340, font_size=22),
        TextSlot(id="slot.choice.na", text="㉯ 선분 ㅇㄴ", style_role="choice", x=325, y=340, font_size=22),
        TextSlot(id="slot.choice.da", text="㉰ 선분 ㅇㄷ", style_role="choice", x=555, y=340, font_size=22),
        TextSlot(id="slot.choice.ra", text="㉱ 선분 ㅇㅁ", style_role="choice", x=90, y=400, font_size=22),
        TextSlot(id="slot.choice.ma", text="㉲ 선분 ㄹㅂ", style_role="choice", x=325, y=400, font_size=22),
        TextSlot(id="slot.choice.ba", text="㉳ 선분 ㄴㅅ", style_role="choice", x=555, y=400, font_size=22),
    )

    return ProblemTemplate(
        id="S3_초등_3_008644",
        title="원의 반지름 고르기",
        canvas=Canvas(width=746, height=537, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=tuple(slot.id for slot in stem_slots)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(slot.id for slot in diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=tuple(slot.id for slot in choice_slots)),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(*stem_slots, *diagram_slots, *choice_slots),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("circle", "radius", "multiple_select"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008644",
    "problem_type": "geometry_circle_radius_selection",
    "metadata": {
        "language": "ko",
        "question": "점 ㅇ는 원의 중심입니다. 원의 반지름은 어느 선분인지 모두 선택해 보세요.",
        "instruction": "원의 중심 ㅇ와 원 위의 한 점을 이은 선분을 모두 고르는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.center.O", "type": "point", "label": "ㅇ", "role": "center"},
            {"id": "obj.circle", "type": "circle", "center": "obj.center.O"},
            {"id": "obj.segment.ga", "type": "segment", "label": "ㄱㅅ"},
            {"id": "obj.segment.na", "type": "segment", "label": "ㅇㄴ"},
            {"id": "obj.segment.da", "type": "segment", "label": "ㅇㄷ"},
            {"id": "obj.segment.ra", "type": "segment", "label": "ㅇㅁ"},
            {"id": "obj.segment.ma", "type": "segment", "label": "ㄹㅂ"},
            {"id": "obj.segment.ba", "type": "segment", "label": "ㄴㅅ"},
        ],
        "relations": [
            {"id": "rel.radius.na", "type": "radius", "from_id": "obj.center.O", "to_id": "obj.segment.na", "segment": "ㅇㄴ"},
            {"id": "rel.radius.da", "type": "radius", "from_id": "obj.center.O", "to_id": "obj.segment.da", "segment": "ㅇㄷ"},
            {"id": "rel.radius.ra", "type": "radius", "from_id": "obj.center.O", "to_id": "obj.segment.ra", "segment": "ㅇㅁ"},
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.center.O"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.radius.na", "rel.radius.da", "rel.radius.ra"],
            },
            "plan": {
                "method": "definition_match",
                "description": "원의 중심 ㅇ와 원 위의 한 점을 이은 선분인지 확인한다.",
            },
            "execute": {"expected_operations": ["identify_center", "check_endpoint_on_circle", "select_radius_candidates"]},
            "review": {"check_methods": ["definition_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": ["가", "나", "다", "라", "마", "바"],
        "answer_key": ["나", "다", "라"],
        "target": {
            "type": "multiple_choice_selection",
            "description": "원의 반지름인 선분을 모두 고르기",
        },
        "value": "나, 다, 라",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008644",
    "problem_type": "geometry_circle_radius_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "원의 반지름",
        "target_ticks": 0,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {"ref": "obj.center.O", "value": {"label": "ㅇ", "role": "center"}},
        {"ref": "obj.circle", "value": {"type": "circle", "center": "ㅇ"}},
    ],
    "target": {"ref": "answer.target", "type": "multiple_choice_selection"},
    "method": "definition_match",
    "plan": ["원의 중심 ㅇ와 원 위의 한 점을 이은 선분을 찾는다.", "해당하는 보기를 모두 고른다."],
    "steps": [
        {"id": "step.1", "expr": "중심 ㅇ가 포함된 선분 확인", "value": ["ㅇㄴ", "ㅇㄷ", "ㅇㅁ"]},
        {"id": "step.2", "expr": "원 위의 점과 중심 ㅇ를 이은 선분 확인", "value": ["나", "다", "라"]},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 보기 모두가 반지름의 정의에 맞는가",
            "expected": ["나", "다", "라"],
            "actual": ["나", "다", "라"],
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": ["가", "나", "다", "라", "마", "바"],
        "answer_key": ["나", "다", "라"],
        "target": {
            "type": "multiple_choice_selection",
            "description": "원의 반지름인 선분을 모두 고르기",
        },
        "value": "나, 다, 라",
        "unit": "",
    },
}
