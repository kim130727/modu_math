"""ModuMath Problem DSL: 두 반의 표를 합산하여 바르게 말한 사람 선택하기 (S3_초등_3_008886)"""

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


PROBLEM_ID = "S3_초등_3_008886"
PROBLEM_TITLE = "표를 보고 현장 체험 학습 장소에 대해 바르게 말한 사람 선택하기"

ANSWER = {
    "type": "choice",
    "value": "하은",
    "unit": "",
    "answer_index": 0,
    "values": ["하은"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "하은", "value": "하은"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "소율", "value": "소율"},
    ],
    "answer_key": [{"slot_id": "slot.choice.option_0", "value": "하은"}],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_table_aggregation",
    "metadata": {
        "grade": 3,
        "semester": 2,
        "subject": "수학",
        "chapter": "06단원_자료의 정리",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "place.museum", "type": "survey_item", "label": "박물관", "haeun_class": 6, "soyul_class": 10, "total": 16},
            {"id": "place.art", "type": "survey_item", "label": "미술관", "haeun_class": 7, "soyul_class": 2, "total": 9},
            {"id": "place.botanical", "type": "survey_item", "label": "식물원", "haeun_class": 9, "soyul_class": 8, "total": 17},
            {"id": "place.science", "type": "survey_item", "label": "과학관", "haeun_class": 5, "soyul_class": 3, "total": 8},
            {"id": "person.haeun", "type": "speaker", "name": "하은", "claim": "식물원"},
            {"id": "person.soyul", "type": "speaker", "name": "소율", "claim": "박물관"},
        ],
        "relations": [
            {
                "id": "relation.correct_speaker",
                "type": "correctly_interprets",
                "from_id": "person.haeun",
                "to_id": "place.botanical",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="50. 하은이네 반과 소율이네 반은 함께 현장 체험 학습을 가려고 학생들이 가고 싶어 하는 장소를 조사하여 표로 나타내었습니다. 하은이네 반과 소율이네 반이 어디로 현장 체험 학습을 가면 좋을지 바르게 말한 사람을 선택해 보세요.",
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

    table_title = TextSlot(id="slot.diagram.table_title", prompt="", text="현장 체험 학습으로 가고 싶어 하는 장소", x=443, y=104, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    tbl = table_slots(
        "slot.diagram.table",
        x=98,
        y=124,
        col_widths=(260, 86, 86, 86, 86, 86),
        row_heights=(38, 38, 38),
        cells=(
            ("장소", "박물관", "미술관", "식물원", "과학관", "합계"),
            ("하은이네 반 학생 수(명)", "6", "7", "9", "5", "27"),
            ("소율이네 반 학생 수(명)", "10", "2", "8", "3", "23"),
        ),
        font_size=18,
        stroke="#65a30d",
    )

    # 하은 말풍선 및 이름표
    bubble_haeun = RectSlot(id="slot.diagram.bubble_haeun", prompt="", x=95, y=262, width=275, height=118, fill="#ffffff", stroke="#475569", stroke_width=1.4)
    text_haeun = TextBoxSlot(
        id="slot.diagram.text_haeun",
        prompt="",
        text="가고 싶은 장소별\n두 반의 학생 수를 합한 수가\n가장 큰 식물원으로\n가면 좋을 것 같아.",
        x=105,
        y=272,
        width=255,
        height=98,
        font_size=16,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
        line_height=1.35,
    )
    head_haeun = CircleSlot(id="slot.diagram.head_haeun", prompt="", cx=405, cy=325, r=18, fill="#fde68a", stroke="#d97706", stroke_width=1.2)
    name_box_haeun = RectSlot(id="slot.choice.option_0", prompt="", x=332, y=362, width=72, height=34, fill="#ffffff", stroke="#64748b", stroke_width=1.3, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "하은", "group_id": "slot.choice.group", "include_in_submission": True})
    name_haeun = TextSlot(id="slot.choice.label_0", prompt="", text="하은", x=368, y=379, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    # 소율 말풍선 및 이름표
    bubble_soyul = RectSlot(id="slot.diagram.bubble_soyul", prompt="", x=548, y=256, width=275, height=118, fill="#ffffff", stroke="#475569", stroke_width=1.4)
    text_soyul = TextBoxSlot(
        id="slot.diagram.text_soyul",
        prompt="",
        text="우리 반 학생들이\n가장 많이 가고 싶어 하는\n박물관으로 가면\n좋을 것 같아.",
        x=558,
        y=266,
        width=255,
        height=98,
        font_size=16,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
        line_height=1.35,
    )
    head_soyul = CircleSlot(id="slot.diagram.head_soyul", prompt="", cx=510, cy=325, r=18, fill="#fde68a", stroke="#d97706", stroke_width=1.2)
    name_box_soyul = RectSlot(id="slot.choice.option_1", prompt="", x=546, y=362, width=72, height=34, fill="#ffffff", stroke="#64748b", stroke_width=1.3, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "소율", "group_id": "slot.choice.group", "include_in_submission": True})
    name_soyul = TextSlot(id="slot.choice.label_1", prompt="", text="소율", x=582, y=379, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    diagram_slots = (table_title, *tbl, bubble_haeun, text_haeun, head_haeun, bubble_soyul, text_soyul, head_soyul)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=415, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.option_0", "slot.choice.label_0", "slot.choice.option_1", "slot.choice.label_1"),
            ),
        ),
        slots=(stem_slot, *diagram_slots, name_box_haeun, name_haeun, name_box_soyul, name_soyul),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "place.museum", "value": [6, 10]},
        {"ref": "place.art", "value": [7, 2]},
        {"ref": "place.botanical", "value": [9, 8]},
        {"ref": "place.science", "value": [5, 3]},
    ],
    "target": {"ref": "slot.choice.option_0", "type": "choice"},
    "method": "sum_two_classes_and_compare",
    "steps": [
        {"id": "step.sum_museum", "expr": "6 + 10", "value": 16, "explanation": "박물관은 6 + 10 = 16명입니다."},
        {"id": "step.sum_art", "expr": "7 + 2", "value": 9, "explanation": "미술관은 7 + 2 = 9명입니다."},
        {"id": "step.sum_botanical", "expr": "9 + 8", "value": 17, "explanation": "식물원은 9 + 8 = 17명입니다."},
        {"id": "step.sum_science", "expr": "5 + 3", "value": 8, "explanation": "과학관은 5 + 3 = 8명입니다."},
        {"id": "step.compare", "expr": "max(16, 9, 17, 8) == 17", "value": "하은", "explanation": "두 반의 학생 수를 합한 수가 가장 큰 장소는 식물원(17명)이므로 바르게 말한 사람은 하은입니다."},
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["data.two_way_table_aggregation"],
        "errors": {
            "소율": "data.considered_only_one_class",
        },
    },
}
