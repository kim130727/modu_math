from __future__ import annotations

from modu_math.dsl import (
    Arrow,
    BlankSlot,
    Canvas,
    ChoiceSlot,
    Circle,
    CircleSlot,
    Constraint,
    Cube,
    DiagramTemplate,
    FractionAreaModel,
    Grid,
    Group,
    ImageSlot,
    LabelSlot,
    LineSlot,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    ShapeObject,
    TextBoxSlot,
    TextSlot,
    Triangle,
)


def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=673.0,
        height=401.0,
        coordinate_mode="logical",
    )
    regions = (
        Region(
            id="region.stem",
            role="stem",
            flow="absolute",
            slot_ids=("slot.q_text",),
        ),
        Region(
            id="region.diagram",
            role="diagram",
            flow="absolute",
            slot_ids=(
                "slot.circle.outer",
                "slot.circle.center",
                "slot.line.top",
                "slot.line.middle1",
                "slot.line.middle2",
                "slot.line.bottom",
                "slot.lb.giyeok",
                "slot.lb.nieun",
                "slot.lb.digeut",
                "slot.lb.rieul",
                "slot.lb.mieum",
                "slot.lb.bieup",
                "slot.lb.sieut1",
                "slot.lb.sieut2",
                "slot.dot.center",
            ),
        ),
        Region(
            id="region.options",
            role="choices",
            flow="absolute",
            slot_ids=("slot.opt1", "slot.opt2", "slot.opt3", "slot.opt4"),
        ),
        Region(
            id="region.answer",
            role="answer",
            flow="absolute",
            slot_ids=(),
        ),
    )
    slots = (
        TextSlot(
            id="slot.q_text",
            prompt="",
            text="最も長い線分はどれですか。",
            style_role="question",
            x=40,
            y=35,
            font_size=30,
        ),
        CircleSlot(
            id="slot.circle.outer",
            prompt="",
            cx=320,
            cy=170,
            r=105,
            fill="none",
        ),
        CircleSlot(
            id="slot.circle.center",
            prompt="",
            cx=330,
            cy=150,
            r=5,
            fill="none",
        ),
        LineSlot(
            id="slot.line.top",
            prompt="",
            x1=230,
            y1=115,
            x2=410,
            y2=115,
        ),
        LineSlot(
            id="slot.line.middle1",
            prompt="",
            x1=237,
            y1=235,
            x2=402,
            y2=235,
        ),
        LineSlot(
            id="slot.line.middle2",
            prompt="",
            x1=215,
            y1=170,
            x2=425,
            y2=170,
        ),
        LineSlot(
            id="slot.line.bottom",
            prompt="",
            x1=220,
            y1=205,
            x2=420,
            y2=205,
        ),
        TextSlot(
            id="slot.lb.giyeok",
            prompt="",
            text="ア",
            style_role="label",
            x=195,
            y=120,
            font_size=25,
        ),
        TextSlot(
            id="slot.lb.nieun",
            prompt="",
            text="イ",
            style_role="label",
            x=420,
            y=120,
            font_size=25,
        ),
        TextSlot(
            id="slot.lb.digeut",
            prompt="",
            text="ウ",
            style_role="label",
            x=180,
            y=175,
            font_size=25,
        ),
        TextSlot(
            id="slot.lb.rieul",
            prompt="",
            text="エ",
            style_role="label",
            x=435,
            y=175,
            font_size=25,
        ),
        TextSlot(
            id="slot.lb.mieum",
            prompt="",
            text="オ",
            style_role="label",
            x=190,
            y=215,
            font_size=25,
        ),
        TextSlot(
            id="slot.lb.bieup",
            prompt="",
            text="カ",
            style_role="label",
            x=430,
            y=215,
            font_size=25,
        ),
        TextSlot(
            id="slot.lb.sieut1",
            prompt="",
            text="ケ",
            style_role="label",
            x=410,
            y=245,
            font_size=25,
        ),
        TextSlot(
            id="slot.lb.sieut2",
            prompt="",
            text="キ",
            style_role="label",
            x=200,
            y=250,
            font_size=25,
        ),
        CircleSlot(
            id="slot.dot.center",
            prompt="",
            cx=320,
            cy=170,
            r=5,
            fill="#ff1493",
        ),
        TextSlot(
            id="slot.opt1",
            prompt="",
            text="① 線分アイ",
            style_role="choice",
            x=50,
            y=325,
            font_size=30,
        ),
        TextSlot(
            id="slot.opt2",
            prompt="",
            text="② 線分ウエ",
            style_role="choice",
            x=240,
            y=325,
            font_size=30,
        ),
        TextSlot(
            id="slot.opt3",
            prompt="",
            text="③ 線分オカ",
            style_role="choice",
            x=420,
            y=325,
            font_size=30,
        ),
        TextSlot(
            id="slot.opt4",
            prompt="",
            text="④ 線分キケ",
            style_role="choice",
            x=50,
            y=370,
            font_size=30,
        ),
    )
    diagrams = ()
    groups = ()
    constraints = ()
    return ProblemTemplate(
        id="S3_elem_3_008661",
        title="最も長い線分はどれですか。",
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )


PROBLEM_TEMPLATE = build_problem_template()

PROBLEM_ID = "S3_elem_3_008661"

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_elem_3_008661",
    "problem_type": "geometry_segment_comparison",
    "metadata": {
        "language": "ko",
        "question": "길이가 가장 긴 선분은 어느 것인가요?",
        "instruction": "도형을 보고 보기 중 맞는 선분을 고르기",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.segment.gn", "type": "segment", "label": "アイ"},
            {"id": "obj.segment.dr", "type": "segment", "label": "ウエ"},
            {"id": "obj.segment.mb", "type": "segment", "label": "オカ"},
            {"id": "obj.segment.ss", "type": "segment", "label": "キキ"},
            {"id": "obj.center_mark", "type": "mark", "description": "작은 원/점 표시"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.segment.gn",
                    "obj.segment.dr",
                    "obj.segment.mb",
                    "obj.segment.ss",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.dr_passes_center", "rel.max_length"],
            },
            "plan": {
                "method": "visual_comparison",
                "description": "원 안의 선분들 중 중심을 지나는 선분을 찾고, 보기에서 해당 선분을 "
                "고른다.",
            },
            "execute": {
                "expected_operations": ["identify_center_passing_segment", "match_with_choice"]
            },
            "review": {"check_methods": ["compare_with_printed_explanation"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": ["1. 선분 アイ", "2. 선분 ウエ", "3. 선분 オカ", "4. 선분 キケ"],
        "answer_key": ["2. 선분 ウエ"],
        "target": {"type": "choice_selection", "description": "길이가 가장 긴 선분"},
        "value": "2. 선분 ウエ",
        "unit": "",
    },
}

SEMANTIC = SEMANTIC_OVERRIDE

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_elem_3_008661",
    "problem_type": "geometry_segment_comparison",
    "inputs": {
        "total_ticks": 0,
        "target_label": "가장 긴 선분",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.segment.gn", "value": {"label": "선분 アイ"}},
        {"ref": "obj.segment.dr", "value": {"label": "선분 ウエ"}},
        {"ref": "obj.segment.mb", "value": {"label": "선분 オカ"}},
        {"ref": "obj.segment.ss", "value": {"label": "선분 キケ"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_selection"},
    "method": "visual_comparison",
    "plan": [
        "円の中の4本の線分を比べます。",
        "中心を通る線分を探します。",
        "その線分に当たる番号を選びます。",
    ],
    "steps": [
        {"id": "step.1", "expr": "중심을 지나는 선분 확인", "value": "선분 ウエ"},
        {"id": "step.2", "expr": "보기와 대응", "value": "2. 선분 ウエ"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "해설 문장과 선택지 일치 여부",
            "expected": "2. 선분 ウエ",
            "actual": "2. 선분 ウエ",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": ["1. 선분 アイ", "2. 선분 ウエ", "3. 선분 オカ", "4. 선분 キケ"],
        "answer_key": ["2. 선분 ウエ"],
        "target": {"type": "choice_selection", "description": "길이가 가장 긴 선분"},
        "value": "2. 선분 ウエ",
        "unit": "",
    },
}

SEMANTIC_ANSWER = SOLVABLE.get("answer")
