from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, ProblemTemplate, Region, TextSlot, LineSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008699",
        title="원의 지름을 나타내는 선분",
        canvas=Canvas(width=848, height=400, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle",
                    "slot.line.top",
                    "slot.line.mid",
                    "slot.line.bottom",
                    "slot.label.ga",
                    "slot.label.na",
                    "slot.label.da",
                    "slot.label.ra",
                    "slot.label.ma",
                    "slot.label.ba",
                    "slot.label.o",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.1",
                    "slot.choice.2",
                    "slot.choice.3",
                    "slot.choice.4",
                    "slot.pt.center",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="원의 지름을 나타내는 선분은 어느 것인가요?",
                style_role="question",
                x=10.0,
                y=32.0,
                font_size=28,
            ),
            CircleSlot(id="slot.circle", prompt="", cx=320, cy=155, r=100, fill="none"),
            CircleSlot(id="slot.pt.center", prompt="", cx=325, cy=150, r=5, fill="#e91e63"),
            LineSlot(id="slot.line.top", prompt="", x1=245, y1=90, x2=395, y2=90),
            LineSlot(id="slot.line.mid", prompt="", x1=220, y1=150, x2=420, y2=150),
            LineSlot(id="slot.line.bottom", prompt="", x1=245, y1=220, x2=395, y2=220),
            TextSlot(
                id="slot.label.ga",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=215,
                y=90,
                font_size=25,
            ),
            TextSlot(
                id="slot.label.na",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=410,
                y=90,
                font_size=25,
            ),
            TextSlot(
                id="slot.label.da",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=180,
                y=160,
                font_size=25,
            ),
            TextSlot(
                id="slot.label.ra",
                prompt="",
                text="ㄹ",
                style_role="label",
                x=435,
                y=155,
                font_size=25,
            ),
            TextSlot(
                id="slot.label.ma",
                prompt="",
                text="ㅁ",
                style_role="label",
                x=205,
                y=225,
                font_size=25,
            ),
            TextSlot(
                id="slot.label.ba",
                prompt="",
                text="ㅂ",
                style_role="label",
                x=415,
                y=235,
                font_size=25,
            ),
            TextSlot(
                id="slot.label.o",
                prompt="",
                text="ㅇ",
                style_role="label",
                x=325,
                y=135,
                font_size=25,
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="① 선분 ㄱㄴ",
                style_role="choice",
                x=25,
                y=315,
                font_size=30,
            ),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text="② 선분 ㄷㄹ",
                style_role="choice",
                x=210,
                y=315,
                font_size=30,
            ),
            TextSlot(
                id="slot.choice.3",
                prompt="",
                text="③ 선분 ㅁㅂ",
                style_role="choice",
                x=25,
                y=365,
                font_size=30,
            ),
            TextSlot(
                id="slot.choice.4",
                prompt="",
                text="④ 선분 ㄷㅇ",
                style_role="choice",
                x=210,
                y=370,
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
    "problem_id": "S3_초등_3_008699",
    "problem_type": "geometry_circle_diameter_mcq",
    "metadata": {
        "language": "ko",
        "question": "원의 지름을 나타내는 선분은 어느 것인가요?",
        "instruction": "알맞은 보기를 고르시오.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.segment_top", "type": "segment", "label_pair": ["ㄱ", "ㄴ"]},
            {"id": "obj.segment_mid", "type": "segment", "label_pair": ["ㄷ", "ㄹ"]},
            {"id": "obj.segment_bottom", "type": "segment", "label_pair": ["ㅁ", "ㅂ"]},
            {"id": "obj.marker_o", "type": "marker", "label": "ㅇ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.segment_top",
                    "obj.segment_mid",
                    "obj.segment_bottom",
                ],
                "target_ref": "answer.target",
                "condition_refs": [
                    "rel.segment_inside_circle",
                    "rel.segment_inside_circle_2",
                    "rel.segment_inside_circle_3",
                ],
            },
            "plan": {
                "method": "compare_segments_in_circle",
                "description": "원 안의 선분들 중 지름의 뜻에 맞는 선분을 찾는다.",
            },
            "execute": {
                "expected_operations": ["compare_lengths_visually", "match_diameter_definition"]
            },
            "review": {"check_methods": ["definition_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "multiple_choice", "description": "원의 지름을 나타내는 선분"},
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008699",
    "problem_type": "geometry_circle_diameter_mcq",
    "inputs": {
        "total_ticks": 4,
        "target_label": "원의 지름을 나타내는 선분",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.segment_top", "value": {"label_pair": ["ㄱ", "ㄴ"]}},
        {"ref": "obj.segment_mid", "value": {"label_pair": ["ㄷ", "ㄹ"]}},
        {"ref": "obj.segment_bottom", "value": {"label_pair": ["ㅁ", "ㅂ"]}},
    ],
    "target": {"ref": "answer.target", "type": "multiple_choice"},
    "method": "definition_match_check",
    "plan": [
        "원 안의 선분들을 보고 지름의 뜻에 맞는 선분을 찾는다.",
        "보기와 대응되는 선분 이름을 확인한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "원 안의 선분 후보를 확인한다.", "value": 3},
        {"id": "step.2", "expr": "지름에 해당하는 보기 번호를 확인한다.", "value": 2},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "보기 ②가 선분 ㄷㄹ과 대응하는지 확인",
            "expected": 2,
            "actual": 2,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "multiple_choice", "description": "원의 지름을 나타내는 선분"},
        "value": 2,
        "unit": "",
    },
}
