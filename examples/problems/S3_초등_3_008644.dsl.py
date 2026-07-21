from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    stem_slots = (
        TextSlot(
            id="slot.question.line1",
            text = '점 ㅇ는 원의 중심입니다. 원의 반지름은 어느 선분인지 모두 선택해 보세요.', style_role="question",
            x = 40, y = 50, font_size = 25),
        
    )

    diagram_slots = (
        CircleSlot(id="slot.figure.circle", cx = 380, cy = 190, r = 90, fill="none", stroke="#333333", stroke_width=1.3),
        LineSlot(id="slot.segment.ga", x1 = 324, y1 = 118, x2 = 429, y2 = 113, stroke="#333333", stroke_width=1.3),
        LineSlot(id="slot.segment.na_to_sa", x1 = 300, y1 = 150, x2 = 430, y2 = 115, stroke = '#333333', stroke_width = 1.3),
        LineSlot(id="slot.segment.la_ba", x1 = 430, y1 = 266, x2 = 450, y2 = 136, stroke="#333333", stroke_width=1.3),
        LineSlot(id="slot.segment.o_na", x1 = 380, y1 = 190, x2 = 300, y2 = 150, stroke="#333333", stroke_width=1.3, transform = 'rotate(-5 340 170)'),
        LineSlot(id="slot.segment.o_da", x1 = 390, y1 = 195, x2 = 330, y2 = 265, stroke="#333333", stroke_width=1.3, transform = 'rotate(-15 370 225)'),
        LineSlot(id="slot.segment.o_ma", x1 = 384, y1 = 188, x2 = 469, y2 = 188, stroke="#333333", stroke_width=1.3),
        CircleSlot(id="slot.center.dot", cx = 384, cy = 188, r = 5, fill="#ec2aa0", stroke="#ec2aa0", stroke_width=1),
        TextSlot(id="slot.label.giyeok", text = 'ㄱ', style_role="label", x = 300, y = 110, font_size = 15),
        TextSlot(id="slot.label.siot", text = 'ㅅ', style_role="label", x = 435, y = 115, font_size = 15),
        TextSlot(id="slot.label.bieup", text = 'ㅂ', style_role="label", x = 460, y = 135, font_size = 15),
        TextSlot(id="slot.label.nieun", text = 'ㄴ', style_role="label", x = 275, y = 150, font_size = 15),
        TextSlot(id="slot.label.mieum", text = 'ㅁ', style_role="label", x = 474, y = 193, font_size = 15),
        TextSlot(id="slot.label.digeut", text = 'ㄷ', style_role="label", x = 300, y = 285, font_size = 15),
        TextSlot(id="slot.label.rieul", text = 'ㄹ', style_role="label", x = 425, y = 295, font_size = 15, fill = '#111111'),
        
    )

    choice_slots = (
        TextSlot(id="slot.choice.ga", text = '㉮ 선분 ㄱㅅ', style_role="choice", x = 90, y = 330, font_size = 20),
        TextSlot(id="slot.choice.na", text = '㉯ 선분 ㅇㄴ', style_role="choice", x = 325, y = 335, font_size = 20),
        TextSlot(id="slot.choice.da", text = '㉰ 선분 ㅇㄷ', style_role="choice", x = 535, y = 335, font_size = 20),
        TextSlot(id="slot.choice.ra", text = '㉱ 선분 ㅇㅁ', style_role="choice", x = 90, y = 390, font_size = 20),
        TextSlot(id="slot.choice.ma", text = '㉲ 선분 ㄹㅂ', style_role="choice", x = 325, y = 395, font_size = 20),
        TextSlot(id="slot.choice.ba", text = '㉳ 선분 ㄴㅅ', style_role="choice", x = 535, y = 395, font_size = 20),
    )

    answer_slots = (
        
    )

    return ProblemTemplate(
        id="S3_초등_3_008644",
        title="원의 반지름 고르기",
        canvas=Canvas(width=746, height=537, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=tuple(slot.id for slot in stem_slots)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=(tuple(slot.id for slot in diagram_slots), )),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=(tuple(slot.id for slot in choice_slots), 'slot.choice.na.copy2')),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=tuple(slot.id for slot in answer_slots)),
        ),
        slots=(*stem_slots, *diagram_slots, *choice_slots, *answer_slots, TextSlot(id = 'slot.choice.na.copy2', prompt = '', text = 'ㅇ', x = 385, y = 215, font_size = 20, fill = '#111111')),
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
        "question": "점 O는 원의 중심입니다. 원의 반지름은 어느 선분인지 모두 선택해 보세요.",
        "instruction": "원의 중심 O와 원 위의 한 점을 이은 선분을 모두 고르는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.center.O", "type": "point", "label": "O", "role": "center"},
            {"id": "obj.circle", "type": "circle", "center": "obj.center.O"},
            {"id": "obj.segment.ga", "type": "segment", "label": "ㄱㅅ"},
            {"id": "obj.segment.na", "type": "segment", "label": "Oㄴ"},
            {"id": "obj.segment.da", "type": "segment", "label": "Oㄷ"},
            {"id": "obj.segment.ra", "type": "segment", "label": "Oㅁ"},
            {"id": "obj.segment.ma", "type": "segment", "label": "ㄹㅂ"},
            {"id": "obj.segment.ba", "type": "segment", "label": "ㄴㅅ"},
        ],
        "relations": [
            {"id": "rel.radius.na", "type": "radius", "segment": "Oㄴ"},
            {"id": "rel.radius.da", "type": "radius", "segment": "Oㄷ"},
            {"id": "rel.radius.ra", "type": "radius", "segment": "Oㅁ"},
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.center.O"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.radius.na", "rel.radius.da", "rel.radius.ra"],
            },
            "plan": {
                "method": "definition_match",
                "description": "원의 중심 O와 원 위의 한 점을 이은 선분인지 확인한다.",
            },
            "execute": {"expected_operations": ["identify_center", "check_endpoint_on_circle", "select_radius_candidates"]},
            "review": {"check_methods": ["definition_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "multiple_choice_selection",
            "description": "원의 반지름인 선분을 모두 고르기",
            "choices": ["㉯", "㉰", "㉱"],
        },
        "value": "㉯, ㉰, ㉱",
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
        {"ref": "obj.center.O", "value": {"label": "O", "role": "center"}},
        {"ref": "obj.circle", "value": {"type": "circle", "center": "O"}},
    ],
    "target": {"ref": "answer.target", "type": "multiple_choice_selection"},
    "method": "definition_match",
    "plan": ["원의 중심 O와 원 위의 한 점을 이은 선분을 찾는다.", "해당하는 보기를 모두 고른다."],
    "steps": [
        {"id": "step.1", "expr": "중심 O가 포함된 선분 확인", "value": ["Oㄴ", "Oㄷ", "Oㅁ"]},
        {"id": "step.2", "expr": "원 위의 점과 중심 O를 이은 선분 확인", "value": ["㉯", "㉰", "㉱"]},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 보기 모두가 반지름의 정의에 맞는가",
            "expected": ["㉯", "㉰", "㉱"],
            "actual": ["㉯", "㉰", "㉱"],
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "multiple_choice_selection",
            "description": "원의 반지름인 선분을 모두 고르기",
            "choices": ["㉯", "㉰", "㉱"],
        },
        "value": "㉯, ㉰, ㉱",
        "unit": "",
    },
}
