"""ModuMath Problem DSL: 클립의 두께에 알맞은 단위 선택하기 (S3_초등_3_009173)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    PathSlot,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009173"
PROBLEM_TITLE = "표시된 길이에 알맞은 단위 선택하기 (클립)"

ANSWER = {
    "type": "choice",
    "value": "mm",
    "unit": "",
    "answer_index": 1,
    "values": ["mm"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "cm", "value": "cm"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "mm", "value": "mm"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "mm",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_unit_estimation",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "05단원_길이와 시간",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "object.paperclip_width", "type": "measured_length", "label": "클립의 폭", "numeric_value": 8},
        ],
        "relations": [
            {
                "id": "relation.appropriate_unit",
                "type": "has_unit",
                "from_id": "object.paperclip_width",
                "to_id": "unit.mm",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="35. 알맞은 단위에 ○표 하세요.",
        x=32,
        y=22,
        width=820,
        height=44,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    # 클립 도형 및 오른쪽 폭 표시선
    clip_outer = PathSlot(
        id="slot.diagram.clip_outer",
        prompt="",
        d="M 455 82 L 595 82 A 16 16 0 0 1 595 114 L 460 114 A 16 16 0 0 1 460 82",
        fill="none",
        stroke="#64748b",
        stroke_width=4.0,
    )
    clip_inner = PathSlot(
        id="slot.diagram.clip_inner",
        prompt="",
        d="M 595 90 L 490 90 A 8 8 0 0 0 490 106 L 575 106",
        fill="none",
        stroke="#94a3b8",
        stroke_width=3.5,
    )
    dim_top = LineSlot(id="slot.diagram.dim_top", prompt="", x1=612, y1=82, x2=628, y2=82, stroke="#ec4899", stroke_width=1.5)
    dim_bot = LineSlot(id="slot.diagram.dim_bot", prompt="", x1=612, y1=114, x2=628, y2=114, stroke="#ec4899", stroke_width=1.5)
    dim_vert = LineSlot(id="slot.diagram.dim_vert", prompt="", x1=620, y1=82, x2=620, y2=114, stroke="#ec4899", stroke_width=1.5)

    sent_left = TextSlot(id="slot.diagram.sent_left", prompt="", text="표시된 길이는 8 (", x=382, y=158, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="cm",
        x=518,
        y=158,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "cm", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    comma_1 = TextSlot(id="slot.choice.comma_1", prompt="", text=",", x=552, y=158, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="mm",
        x=590,
        y=158,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "mm", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    sent_right = TextSlot(id="slot.diagram.sent_right", prompt="", text=")입니다.", x=668, y=158, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    diagram_slots = (clip_outer, clip_inner, dim_top, dim_bot, dim_vert, sent_left, sent_right)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=195, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.comma_1", "slot.choice.option_1")),
        ),
        slots=(stem_slot, *diagram_slots, opt_0, comma_1, opt_1),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "object.paperclip_width", "value": 8},
    ],
    "target": {"ref": "slot.choice.option_1", "type": "choice"},
    "method": "estimate_appropriate_length_unit",
    "steps": [
        {
            "id": "step.estimate",
            "expr": "width(paperclip) < 1 cm",
            "value": "mm",
            "explanation": "표시된 클립의 폭은 1 cm보다 짧으므로 알맞은 단위는 mm입니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["measurement.unit_estimation_mm_cm"],
        "errors": {
            "cm": "measurement.overestimated_small_object",
        },
    },
}
