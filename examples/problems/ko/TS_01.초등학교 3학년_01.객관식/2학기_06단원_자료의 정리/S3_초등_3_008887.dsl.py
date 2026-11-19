"""ModuMath Problem DSL: 조사한 자료와 표의 편리함 비교하기 (S3_초등_3_008887)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
    table_slots,
)


PROBLEM_ID = "S3_초등_3_008887"
PROBLEM_TITLE = "조사한 자료와 표 중 편리한 것 선택하기"

ANSWER = {
    "type": "choice",
    "value": "표",
    "unit": "",
    "answer_index": 1,
    "values": ["표"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "조사한 자료", "value": "조사한 자료"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "표", "value": "표"},
    ],
    "answer_key": [{"slot_id": "slot.choice.option_1", "value": "표"}],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_data_representation_comparison",
    "metadata": {
        "grade": 3,
        "semester": 2,
        "subject": "수학",
        "chapter": "06단원_자료의 정리",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "rep.raw_data", "type": "data_representation", "label": "조사한 자료", "is_summarized": False},
            {"id": "rep.table", "type": "data_representation", "label": "표", "is_summarized": True},
        ],
        "relations": [
            {
                "id": "relation.convenience",
                "type": "more_convenient_for_reading_counts",
                "from_id": "rep.table",
                "to_id": "rep.raw_data",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="51. 지은이네 학교 3학년 학생들이 태어난 계절을 조사하였습니다. 계절별 태어난 여학생 수와 남학생 수를 알아보려고 할 때 조사한 자료와 표 중에서 어느 것이 더 편리할까요?",
        x=32,
        y=16,
        width=820,
        height=76,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.45,
    )

    # 조사한 자료 요약 상자 (계절별 점 자료)
    raw_bg = RectSlot(id="slot.diagram.raw_bg", prompt="", x=175, y=104, width=540, height=130, fill="#d1fae5", stroke="#6ee7b7", stroke_width=1.2)
    raw_title = TextSlot(id="slot.diagram.raw_title", prompt="", text="태어난 계절", x=445, y=116, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    seasons = ("봄", "여름", "가을", "겨울")
    season_slots = []
    for idx, name in enumerate(seasons):
        bx = 190 + idx * 130
        season_slots.append(RectSlot(id=f"slot.diagram.raw_box_{idx}", prompt="", x=bx, y=134, width=116, height=90, fill="#ffffff", stroke="#a78bfa", stroke_width=1.0))
        season_slots.append(TextSlot(id=f"slot.diagram.raw_lbl_{idx}", prompt="", text=name, x=bx + 58, y=146, font_size=15, font_family='"Noto Sans KR", sans-serif', fill="#4c1d95", align="center"))
        for d in range(6):
            cx = bx + 22 + (d % 3) * 34
            cy = 172 + (d // 3) * 26
            color = "#f472b6" if (d + idx) % 2 == 0 else "#38bdf8"
            season_slots.append(CircleSlot(id=f"slot.diagram.raw_dot_{idx}_{d}", prompt="", cx=cx, cy=cy, r=5, fill=color, stroke="none", stroke_width=0))

    legend_g_dot = CircleSlot(id="slot.diagram.legend_g_dot", prompt="", cx=585, cy=246, r=5, fill="#f472b6", stroke="none", stroke_width=0)
    legend_g_txt = TextSlot(id="slot.diagram.legend_g_txt", prompt="", text=": 여학생", x=622, y=246, font_size=14, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    legend_b_dot = CircleSlot(id="slot.diagram.legend_b_dot", prompt="", cx=672, cy=246, r=5, fill="#38bdf8", stroke="none", stroke_width=0)
    legend_b_txt = TextSlot(id="slot.diagram.legend_b_txt", prompt="", text=": 남학생", x=708, y=246, font_size=14, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    table_title = TextSlot(id="slot.diagram.table_title", prompt="", text="학생들이 태어난 계절", x=443, y=274, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    tbl = table_slots(
        "slot.diagram.table",
        x=158,
        y=294,
        col_widths=(175, 84, 84, 84, 84, 84),
        row_heights=(36, 36, 36),
        cells=(
            ("계절", "봄", "여름", "가을", "겨울", "합계"),
            ("여학생 수(명)", "11", "6", "20", "17", "54"),
            ("남학생 수(명)", "12", "10", "14", "20", "56"),
        ),
        font_size=18,
        stroke="#8b5cf6",
    )

    paren_l = TextSlot(id="slot.choice.paren_l", prompt="", text="(", x=340, y=428, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_0 = TextSlot(id="slot.choice.option_0", prompt="", text="조사한 자료", x=420, y=428, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "조사한 자료", "group_id": "slot.choice.group", "include_in_submission": True})
    comma_1 = TextSlot(id="slot.choice.comma_1", prompt="", text=",", x=492, y=428, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_1 = TextSlot(id="slot.choice.option_1", prompt="", text="표", x=525, y=428, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "표", "group_id": "slot.choice.group", "include_in_submission": True})
    paren_r = TextSlot(id="slot.choice.paren_r", prompt="", text=")", x=558, y=428, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    diagram_slots = (raw_bg, raw_title, *season_slots, legend_g_dot, legend_g_txt, legend_b_dot, legend_b_txt, table_title, *tbl)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=465, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.paren_l", "slot.choice.option_0", "slot.choice.comma_1", "slot.choice.option_1", "slot.choice.paren_r")),
        ),
        slots=(stem_slot, *diagram_slots, paren_l, opt_0, comma_1, opt_1, paren_r),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "rep.raw_data", "value": "계절별 점 자료"},
        {"ref": "rep.table", "value": "계절별 여학생·남학생 수 표"},
    ],
    "target": {"ref": "slot.choice.option_1", "type": "choice"},
    "method": "compare_data_representations",
    "steps": [
        {
            "id": "step.compare",
            "expr": "is_summarized(표) == True",
            "value": "표",
            "explanation": "표를 보면 계절별 태어난 여학생 수와 남학생 수를 한눈에 알 수 있으므로 표가 더 편리합니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["data.table_utility"],
        "errors": {
            "조사한 자료": "data.confused_raw_with_table",
        },
    },
}
