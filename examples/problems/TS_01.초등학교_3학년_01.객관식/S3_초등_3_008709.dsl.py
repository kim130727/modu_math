from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, CircleSlot, LineSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008709",
        title="원의 지름",
        canvas=Canvas(width=880.0, height=560.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.circle",
                    "slot.circle_label",
                    "slot.note_box",
                    "slot.note1",
                    "slot.note_arrow",
                    "slot.note2",
                    "slot.choice.1",
                    "slot.choice.2",
                    "slot.choice.3",
                    "slot.choice.4",
                    "slot.note2.copy2",
                    "slot.circle_label.copy3",
                    "slot.circle_label.copy4",
                    "slot.circle_label.copy5",
                    "slot.circle_label.copy6",
                    "slot.circle_label.copy7",
                    "slot.circle_label.copy7.copy8",
                    "slot.circle_label.copy6.copy9",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 안에 공통으로 들어갈 선분으로 알맞은 것은\n무엇인가요?  ",
                style_role="question",
                x=30,
                y=49,
                font_size=30,
            ),
            CircleSlot(id="slot.circle", prompt="", cx=472, cy=205, r=130, fill="none"),
            LineSlot(id="slot.circle.line1", prompt="", x1=425, y1=85, x2=350, y2=250),
            LineSlot(id="slot.circle.line2", prompt="", x1=480, y1=75, x2=375, y2=295),
            LineSlot(id="slot.circle.line3", prompt="", x1=525, y1=90, x2=415, y2=320),
            LineSlot(id="slot.circle.line4", prompt="", x1=590, y1=155, x2=510, y2=330),
            CircleSlot(id="slot.circle.center_mark", prompt="", cx=453, cy=205, r=5, fill="none"),
            CircleSlot(id="slot.circle.pink_dot", prompt="", cx=470, cy=205, r=5, fill="#ff4fa0"),
            TextSlot(
                id="slot.circle_label",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=400,
                y=80,
                font_size=20,
            ),
            RectSlot(
                id="slot.note_box", prompt="", x=36, y=354, width=760, height=125, fill="none"
            ),
            TextSlot(
                id="slot.note1",
                prompt="",
                text="선분",
                style_role="note",
                x=56,
                y=399,
                font_size=30,
            ),
            RectSlot(
                id="slot.note1_blank", prompt="", x=121, y=374, width=65, height=30, fill="none"
            ),
            TextSlot(
                id="slot.note_arrow",
                prompt="",
                text="→",
                style_role="note",
                x=76,
                y=454,
                font_size=35,
            ),
            TextSlot(
                id="slot.note2",
                prompt="",
                text="원의 지름은 선분",
                style_role="note",
                x=126,
                y=459,
                font_size=30,
            ),
            RectSlot(
                id="slot.note2_blank", prompt="", x=348, y=434, width=65, height=30, fill="none"
            ),
            TextSlot(
                id="slot.note2_tail",
                prompt="",
                text="입니다.",
                style_role="note",
                x=426,
                y=459,
                font_size=30,
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="① ㄱㄴ",
                style_role="choice",
                x=31,
                y=534,
                font_size=30,
            ),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text="② ㄷㅁ",
                style_role="choice",
                x=156,
                y=534,
                font_size=30,
            ),
            TextSlot(
                id="slot.choice.3",
                prompt="",
                text="③ ㅁㅂ",
                style_role="choice",
                x=291,
                y=534,
                font_size=30,
            ),
            TextSlot(
                id="slot.choice.4",
                prompt="",
                text="④ ㅅㅈ",
                style_role="choice",
                x=439,
                y=534,
                font_size=30,
            ),
            TextSlot(
                id="slot.note2.copy2",
                prompt="",
                text="은 원안에서 그을 수 있는 가장 긴 선분입니다. ",
                x=201,
                y=399,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.circle_label.copy3",
                prompt="",
                text="ㄷ",
                x=470,
                y=70,
                font_size=20,
                fill="#111111",
            ),
            TextSlot(
                id="slot.circle_label.copy4",
                prompt="",
                text="ㄴ",
                x=330,
                y=260,
                font_size=20,
                fill="#111111",
            ),
            TextSlot(
                id="slot.circle_label.copy5",
                prompt="",
                text="ㄹ",
                x=350,
                y=305,
                font_size=20,
                fill="#111111",
            ),
            TextSlot(
                id="slot.circle_label.copy6",
                prompt="",
                text="ㅁ",
                x=525,
                y=80,
                font_size=20,
                fill="#111111",
            ),
            TextSlot(
                id="slot.circle_label.copy7",
                prompt="",
                text="ㅅ",
                x=595,
                y=150,
                font_size=20,
                fill="#111111",
            ),
            TextSlot(
                id="slot.circle_label.copy7.copy8",
                prompt="",
                text="ㅈ",
                x=510,
                y=350,
                font_size=20,
                fill="#111111",
            ),
            TextSlot(
                id="slot.circle_label.copy6.copy9",
                prompt="",
                text="ㅂ",
                x=390,
                y=340,
                font_size=20,
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
    "problem_id": "S3_초등_3_008709",
    "problem_type": "concept_multiple_choice",
    "metadata": {
        "language": "ko",
        "question": "□ 안에 공통으로 들어갈 선분으로 알맞은 것은 무엇인가요?",
        "instruction": "원의 지름의 뜻을 알고 알맞은 선분을 고르는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.diameter", "type": "segment", "property": "longest_segment_in_circle"},
            {"id": "obj.candidate_1", "type": "segment"},
            {"id": "obj.candidate_2", "type": "segment"},
            {"id": "obj.candidate_3", "type": "segment"},
            {"id": "obj.candidate_4", "type": "segment"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.diameter_definition"],
            },
            "plan": {
                "method": "definition_match",
                "description": "원의 지름의 뜻과 보기의 선분 이름을 맞춘다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_definition",
                    "compare_candidates",
                    "select_matching_segment",
                ]
            },
            "review": {"check_methods": ["definition_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "matching_segment_name",
            "description": "두 빈칸에 공통으로 들어갈 선분 이름",
        },
        "value": "ㅁㅂ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008709",
    "problem_type": "concept_multiple_choice",
    "inputs": {
        "total_ticks": 4,
        "target_label": "원의 지름",
        "target_ticks": 1,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.diameter", "value": {"property": "longest_segment_in_circle"}},
    ],
    "target": {"ref": "answer.target", "type": "matching_segment_name"},
    "method": "definition_match",
    "plan": [
        "원의 지름의 뜻을 확인한다.",
        "보기 중 지름에 해당하는 선분 이름을 찾는다.",
        "두 빈칸에 같은 선분 이름이 들어가는지 확인한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "원의 지름 = 원 안에 그을 수 있는 가장 긴 선분",
            "value": "정의 확인",
        },
        {"id": "step.2", "expr": "보기에서 지름에 해당하는 선분을 고른다", "value": "ㅁㅂ"},
        {"id": "step.3", "expr": "두 빈칸에 같은 선분 이름을 넣는다", "value": "ㅁㅂ"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선분 ㅁㅂ가 원 안에 그을 수 있는 가장 긴 선분인지 확인",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "matching_segment_name",
            "description": "두 빈칸에 공통으로 들어갈 선분 이름",
        },
        "value": "ㅁㅂ",
        "unit": "",
    },
}
