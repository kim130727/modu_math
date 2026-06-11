from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PathSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
    character_body_slots,
    circle_fold_sequence_slots,
    speech_balloon_slots,
)


def build_problem_template() -> ProblemTemplate:
    fold_slots = circle_fold_sequence_slots(
        "slot.fold",
        x=96.0,
        y=305.0,
        r=56.0,
        gap=195.0,
        stages=("circle", "half", "opened_horizontal", "folded_diagonal", "opened_cross"),
        show_arrows=True,
        fill="#DFF2F0",
        stroke="#00AFA8",
    )

    return ProblemTemplate(
        id="S3_초등_3_008646",
        title="원을 접어 원의 성질 알아보기",
        canvas=Canvas(width=944, height=654, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.stem", "slot.speech.bubble", "slot.speech.tail", "slot.speech.text"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.fold.stage1.paper",
                    "slot.fold.stage2.paper",
                    "slot.fold.stage3.paper",
                    "slot.fold.stage3.fold_line",
                    "slot.fold.stage4.paper",
                    "slot.fold.stage5.paper",
                    "slot.fold.stage5.fold_line",
                    "slot.fold.stage5.fold_line2",
                    "slot.fold.stage5.center",
                    "slot.note.equal.arrow",
                    "slot.note.equal",
                    "slot.note.center.arrow",
                    "slot.note.center",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=("slot.answer.box", "slot.answer.text")),
        ),
        slots=(
            TextSlot(
                id="slot.stem",
                prompt="",
                text = '원 모양의 종이를 접어 원의 성질을 알아보고 알맞은 말을 선택하세요.', style_role="question",
                x = 55, y = 35, font_size = 20),
            *character_body_slots("slot.person.left", cx=230.0, head_cy=128.0, hair="#3B2417", shirt="#58C7BC"),
            *speech_balloon_slots(
                "slot.speech",
                cx=540.0,
                cy=129.0,
                width=475.0,
                height=160.0,
                tail_x=290.0,
                tail_y=138.0,
                text="원 모양의 종이를 둘로 똑같이 나누어지도록\n접었다가 펼친 다음 다른 방향으로 둘로 똑같이\n나누어지도록 접었다가 펼쳤어.",
                font_size=22,
                text_dy=-24.0,
            ),
            *fold_slots,
            PathSlot(
                id="slot.note.equal.arrow",
                prompt="",
                d="M 500 247 C 492 230, 506 218, 522 228",
                stroke="#00843D",
                stroke_width=2.0,
                fill="none",
            ),
            TextSlot(
                id="slot.note.equal",
                prompt="",
                text="접힌 선의 윗부분과 아랫부분이 똑같아요.",
                style_role="annotation",
                x=531.0,
                y=241.0,
                font_size=16,
                fill="#00843D",
            ),
            PathSlot(
                id="slot.note.center.arrow",
                prompt="",
                d="M 828 374 C 812 350, 826 329, 870 304",
                stroke="#00843D",
                stroke_width=2.0,
                fill="none",
            ),
            TextSlot(
                id="slot.note.center",
                prompt="",
                text="접었을 때 생기는\n선분들이 만나는 점",
                style_role="annotation",
                x=774.0,
                y=386.0,
                font_size=16,
                fill="#00843D",
            ),
            RectSlot(id="slot.answer.box", prompt="", x=103.0, y=423.0, width=756.0, height=118.0, fill="#F9E0DA", stroke="none"),
            TextSlot(
                id="slot.answer.text",
                prompt="",
                text="원을 둘로 똑같이 나누는 선분은 원의 중심을 지나므로\n원의 ( 지름 , 반지름 )입니다.",
                style_role="answer",
                x=481.0,
                y=468.0,
                font_size=25,
                anchor="middle",
            ),
            
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("geometry", "circle", "paper_folding"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008646",
    "problem_type": "geometry_concept_selection",
    "metadata": {
        "language": "ko",
        "title": "원을 접어 원의 성질 알아보기",
        "question": "원 모양의 종이를 접어 원의 성질을 알아보고 알맞은 말을 선택하는 문제",
        "instruction": "알맞은 말을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle_paper", "type": "circle", "description": "원 모양의 종이"},
            {"id": "obj.fold_line", "type": "line_segment", "description": "원을 둘로 똑같이 나누는 접힌 선"},
            {"id": "obj.center", "type": "point", "description": "원의 중심"},
        ],
        "relations": [
            {"id": "rel.divides_equally", "type": "equal_partition", "description": "선분이 원을 둘로 똑같이 나눈다."},
            {"id": "rel.passes_center", "type": "incidence", "description": "선분이 원의 중심을 지난다."},
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle_paper", "obj.fold_line"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.divides_equally", "rel.passes_center"],
            },
            "plan": {
                "method": "concept_matching",
                "description": "원을 둘로 똑같이 나누며 중심을 지나는 선분은 지름임을 확인한다.",
            },
            "execute": {"expected_operations": ["identify_center_passing_segment", "match_to_diameter"]},
            "review": {"check_methods": ["definition_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": ["지름", "반지름"],
        "answer_key": ["지름"],
        "target": {"type": "concept_name", "description": "원을 둘로 똑같이 나누는 선분의 이름"},
        "value": "지름",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008646",
    "problem_type": "geometry_concept_selection",
    "inputs": {"target_label": "지름", "target_count": 1, "unit": ""},
    "given": [
        {"ref": "obj.circle_paper", "value": {"type": "circle", "description": "원 모양의 종이"}},
        {"ref": "obj.fold_line", "value": {"type": "line_segment", "description": "원을 둘로 똑같이 나누는 접힌 선"}},
    ],
    "target": {"ref": "answer.target", "type": "concept_name"},
    "method": "concept_matching",
    "plan": [
        "접힌 선이 원을 둘로 똑같이 나누는지 확인한다.",
        "그 선이 원의 중심을 지나므로 지름임을 판단한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "원을 둘로 똑같이 나누는 선분은 원의 중심을 지난다.", "value": "center_passing_segment"},
        {"id": "step.2", "expr": "center_passing_segment == diameter", "value": "지름"},
    ],
    "checks": [
        {"id": "check.1", "expr": "원의 중심을 지나는 선분은 지름이다.", "expected": True, "actual": True, "pass": True}
    ],
    "answer": {
        "blanks": [],
        "choices": ["지름", "반지름"],
        "answer_key": ["지름"],
        "target": {"type": "concept_name", "description": "원을 둘로 똑같이 나누는 선분의 이름"},
        "value": "지름",
        "unit": "",
    },
}
