from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008894",
        title="보고 싶은 문화재",
        canvas=Canvas(width=940.0, height=800.0, coordinate_mode="logical"),
        regions=(
            Region(id="region.header", role="stem", flow="absolute", slot_ids=("slot.header",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.title",
                    "slot.panel.outer",
                    "slot.panel.inner",
                    "slot.box.1",
                    "slot.box.2",
                    "slot.box.3",
                    "slot.box.4",
                    "slot.label.1",
                    "slot.label.2",
                    "slot.label.3",
                    "slot.label.4",
                    "slot.legend.pink",
                    "slot.legend.blue",
                    "slot.legend.text1",
                    "slot.legend.text2",
                ),
            ),
            Region(
                id="region.problem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q58", "slot.choice"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.header",
                prompt="",
                text="경수네 학교 3학년 학생들이 보고 싶은 문화재를 조사하였습니다. 물음에 답하세요.",
                style_role="question",
                x=20.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.title",
                prompt="",
                text="보고 싶은 문화재",
                style_role="title",
                x=380.0,
                y=58.0,
                font_size=28,
            ),
            RectSlot(id="slot.panel.outer", x=253.0, y=56.0, width=450.0, height=462.0, prompt=""),
            RectSlot(id="slot.panel.inner", x=263.0, y=66.0, width=430.0, height=442.0, prompt=""),
            RectSlot(id="slot.box.1", x=273.0, y=90.0, width=205.0, height=200.0, prompt=""),
            RectSlot(id="slot.box.2", x=488.0, y=90.0, width=205.0, height=200.0, prompt=""),
            RectSlot(id="slot.box.3", x=273.0, y=300.0, width=205.0, height=200.0, prompt=""),
            RectSlot(id="slot.box.4", x=488.0, y=300.0, width=205.0, height=200.0, prompt=""),
            TextSlot(
                id="slot.label.1",
                prompt="",
                text="첨성대",
                style_role="label",
                x=283.0,
                y=106.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.label.2",
                prompt="",
                text="다보탑",
                style_role="label",
                x=498.0,
                y=106.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.label.3",
                prompt="",
                text="숭례문",
                style_role="label",
                x=283.0,
                y=316.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.label.4",
                prompt="",
                text="종묘",
                style_role="label",
                x=498.0,
                y=316.0,
                font_size=28,
            ),
            CircleSlot(id="slot.legend.pink", prompt="", cx=470.0, cy=540.0, r=7.0, fill="#f2a0bd"),
            CircleSlot(id="slot.legend.blue", prompt="", cx=560.0, cy=540.0, r=7.0, fill="#75c8e5"),
            TextSlot(
                id="slot.legend.text1",
                prompt="",
                text=": 여학생",
                style_role="label",
                x=483.0,
                y=548.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.legend.text2",
                prompt="",
                text=": 남학생",
                style_role="label",
                x=573.0,
                y=548.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q58",
                prompt="",
                text="58. 보고 싶은 문화재별 여학생 수와 남학생 수를 알아보려고 할 때 조사한 자료와 표 중 더 편리한 것을 선택하세요.",
                style_role="question",
                x=20.0,
                y=604.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 조사한 자료 , 표 )",
                style_role="choice",
                x=700.0,
                y=675.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008894",
    "problem_type": "choice",
    "metadata": {
        "language": "ko",
        "question": "보고 싶은 문화재별 여학생 수와 남학생 수를 알아보려고 할 때 조사한 자료와 표 중 더 편리한 것을 고르는 문제",
        "instruction": "더 편리한 것을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.data", "type": "data_display", "name": "조사한 자료"},
            {"id": "obj.table", "type": "data_display", "name": "표"},
            {"id": "obj.subject.female", "type": "group", "name": "여학생"},
            {"id": "obj.subject.male", "type": "group", "name": "남학생"},
            {"id": "obj.culture.1", "type": "cultural_heritage", "name": "첨성대"},
            {"id": "obj.culture.2", "type": "cultural_heritage", "name": "다보탑"},
            {"id": "obj.culture.3", "type": "cultural_heritage", "name": "숭례문"},
            {"id": "obj.culture.4", "type": "cultural_heritage", "name": "종묘"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.data", "obj.table", "obj.subject.female", "obj.subject.male"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_convenience"],
            },
            "plan": {
                "method": "자료비교",
                "description": "문화재별로 여학생 수와 남학생 수를 한눈에 보기 쉬운 자료를 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_organized_information",
                    "select_more_convenient_display",
                ]
            },
            "review": {"check_methods": ["check_if_each_category_can_be_compared_at_a_glance"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "조사한 자료와 표 중 더 편리한 것"},
        "value": "표",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008894",
    "problem_type": "choice",
    "inputs": {
        "total_ticks": 2,
        "target_label": "더 편리한 것",
        "target_ticks": 1,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.data", "value": "조사한 자료"},
        {"ref": "obj.table", "value": "표"},
        {"ref": "obj.subject.female", "value": "여학생"},
        {"ref": "obj.subject.male", "value": "남학생"},
    ],
    "target": {"ref": "answer.target", "type": "choice"},
    "method": "자료비교",
    "plan": [
        "조사한 자료와 표를 비교한다.",
        "문화재별 인원 수를 한눈에 알기 더 편리한 것을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "조사한 자료와 표의 정보 정리 정도를 비교한다.", "value": "표"},
        {
            "id": "step.2",
            "expr": "문화재별 여학생 수와 남학생 수를 한눈에 보기 쉬운 자료를 선택한다.",
            "value": "표",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 자료가 항목별 비교에 더 편리한가",
            "expected": "표",
            "actual": "표",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "조사한 자료와 표 중 더 편리한 것"},
        "value": "표",
        "unit": "",
    },
}
