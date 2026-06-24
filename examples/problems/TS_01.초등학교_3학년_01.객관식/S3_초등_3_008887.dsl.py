from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, CircleSlot, LineSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008887",
        title="태어난 계절과 표",
        canvas=Canvas(width=960.0, height=680.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.problem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.diagram.title",
                    "slot.diagram.outer",
                    "slot.diagram.spring",
                    "slot.diagram.summer",
                    "slot.diagram.autumn",
                    "slot.diagram.winter",
                    "slot.legend.female.dot",
                    "slot.legend.female.text",
                    "slot.legend.male.dot",
                    "slot.legend.male.text",
                    "slot.table.title",
                    "slot.table.outer",
                    "slot.table.head1",
                    "slot.table.head2",
                    "slot.table.head3",
                    "slot.table.head4",
                    "slot.table.head5",
                    "slot.table.head6",
                    "slot.table.row1",
                    "slot.table.r1c1",
                    "slot.table.r1c2",
                    "slot.table.r1c3",
                    "slot.table.r1c4",
                    "slot.table.r1c5",
                    "slot.table.r1c6",
                    "slot.table.r2c1",
                    "slot.table.r2c2",
                    "slot.table.r2c3",
                    "slot.table.r2c4",
                    "slot.table.r2c5",
                    "slot.table.r2c6",
                    "slot.note1",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="51. 지은이는 학교 3학년 학생들이 태어난 계절을 조사하였습니다.\n계절별 태어난 여학생 수와 남학생 수를 알아보려고 할 때 조사한 자료와 표 중에서 어느 것이 더 편리할까요?",
                style_role="question",
                x=16.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.diagram.title",
                prompt="",
                text="태어난 계절",
                style_role="title",
                x=395.0,
                y=142.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.diagram.outer",
                prompt="",
                x=191.0,
                y=148.0,
                width=590.0,
                height=172.0,
                fill="#DDF4F2",
            ),
            RectSlot(
                id="slot.diagram.spring",
                prompt="",
                x=205.0,
                y=180.0,
                width=136.0,
                height=120.0,
                fill="#FFFFFF",
            ),
            RectSlot(
                id="slot.diagram.summer",
                prompt="",
                x=349.0,
                y=180.0,
                width=136.0,
                height=120.0,
                fill="#FFFFFF",
            ),
            RectSlot(
                id="slot.diagram.autumn",
                prompt="",
                x=493.0,
                y=180.0,
                width=136.0,
                height=120.0,
                fill="#FFFFFF",
            ),
            RectSlot(
                id="slot.diagram.winter",
                prompt="",
                x=637.0,
                y=180.0,
                width=136.0,
                height=120.0,
                fill="#FFFFFF",
            ),
            TextSlot(
                id="slot.legend.female.text",
                prompt="",
                text=": 여학생",
                style_role="label",
                x=674.0,
                y=342.0,
                font_size=22,
            ),
            CircleSlot(
                id="slot.legend.female.dot", prompt="", cx=661.0, cy=336.0, r=6.0, fill="#F29AB2"
            ),
            TextSlot(
                id="slot.legend.male.text",
                prompt="",
                text=": 남학생",
                style_role="label",
                x=744.0,
                y=342.0,
                font_size=22,
            ),
            CircleSlot(
                id="slot.legend.male.dot", prompt="", cx=731.0, cy=336.0, r=6.0, fill="#86D5EA"
            ),
            TextSlot(
                id="slot.table.title",
                prompt="",
                text="학생들이 태어난 계절",
                style_role="title",
                x=382.0,
                y=394.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.table.outer",
                prompt="",
                x=172.0,
                y=414.0,
                width=626.0,
                height=126.0,
                fill="#FFFFFF",
            ),
            LineSlot(id="slot.table.head1", prompt="", x1=172.0, y1=446.0, x2=798.0, y2=446.0),
            LineSlot(id="slot.table.head2", prompt="", x1=360.0, y1=414.0, x2=360.0, y2=540.0),
            LineSlot(id="slot.table.head3", prompt="", x1=448.0, y1=414.0, x2=448.0, y2=540.0),
            LineSlot(id="slot.table.head4", prompt="", x1=536.0, y1=414.0, x2=536.0, y2=540.0),
            LineSlot(id="slot.table.head5", prompt="", x1=624.0, y1=414.0, x2=624.0, y2=540.0),
            LineSlot(id="slot.table.head6", prompt="", x1=712.0, y1=414.0, x2=712.0, y2=540.0),
            LineSlot(id="slot.table.row1", prompt="", x1=172.0, y1=478.0, x2=798.0, y2=478.0),
            TextSlot(
                id="slot.table.r1c1",
                prompt="",
                text="계절",
                style_role="label",
                x=229.0,
                y=434.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r1c2",
                prompt="",
                text="봄",
                style_role="label",
                x=404.0,
                y=434.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r1c3",
                prompt="",
                text="여름",
                style_role="label",
                x=490.0,
                y=434.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r1c4",
                prompt="",
                text="가을",
                style_role="label",
                x=578.0,
                y=434.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r1c5",
                prompt="",
                text="겨울",
                style_role="label",
                x=665.0,
                y=434.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r1c6",
                prompt="",
                text="합계",
                style_role="label",
                x=752.0,
                y=434.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r2c1",
                prompt="",
                text="여학생 수(명)",
                style_role="label",
                x=202.0,
                y=468.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r2c2",
                prompt="",
                text="11",
                style_role="label",
                x=404.0,
                y=468.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r2c3",
                prompt="",
                text="6",
                style_role="label",
                x=493.0,
                y=468.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r2c4",
                prompt="",
                text="20",
                style_role="label",
                x=580.0,
                y=468.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r2c5",
                prompt="",
                text="17",
                style_role="label",
                x=667.0,
                y=468.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r2c6",
                prompt="",
                text="54",
                style_role="label",
                x=755.0,
                y=468.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r3c1",
                prompt="",
                text="남학생 수(명)",
                style_role="label",
                x=202.0,
                y=508.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r3c2",
                prompt="",
                text="12",
                style_role="label",
                x=404.0,
                y=508.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r3c3",
                prompt="",
                text="10",
                style_role="label",
                x=493.0,
                y=508.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r3c4",
                prompt="",
                text="14",
                style_role="label",
                x=580.0,
                y=508.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r3c5",
                prompt="",
                text="20",
                style_role="label",
                x=667.0,
                y=508.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.r3c6",
                prompt="",
                text="56",
                style_role="label",
                x=755.0,
                y=508.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.note1",
                prompt="",
                text="( 조사한 자료 , 표 )",
                style_role="note",
                x=360.0,
                y=574.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.dot.spring.f1", prompt="", cx=221.0, cy=228.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.spring.m1", prompt="", cx=238.0, cy=214.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.spring.f2", prompt="", cx=255.0, cy=246.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.spring.m2", prompt="", cx=270.0, cy=226.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.spring.f3", prompt="", cx=287.0, cy=216.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.spring.m3", prompt="", cx=302.0, cy=248.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.spring.f4", prompt="", cx=224.0, cy=264.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.spring.m4", prompt="", cx=245.0, cy=280.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.spring.f5", prompt="", cx=269.0, cy=268.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.spring.m5", prompt="", cx=295.0, cy=264.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.summer.f1", prompt="", cx=366.0, cy=230.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.summer.m1", prompt="", cx=384.0, cy=214.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.summer.f2", prompt="", cx=401.0, cy=246.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.summer.m2", prompt="", cx=420.0, cy=230.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.summer.f3", prompt="", cx=366.0, cy=264.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.summer.m3", prompt="", cx=384.0, cy=280.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.summer.f4", prompt="", cx=421.0, cy=264.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.summer.m4", prompt="", cx=402.0, cy=296.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.autumn.f1", prompt="", cx=510.0, cy=222.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.autumn.m1", prompt="", cx=524.0, cy=210.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.autumn.f2", prompt="", cx=542.0, cy=228.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.autumn.m2", prompt="", cx=555.0, cy=216.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.autumn.f3", prompt="", cx=573.0, cy=222.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.autumn.m3", prompt="", cx=590.0, cy=208.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.autumn.f4", prompt="", cx=508.0, cy=248.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.autumn.m4", prompt="", cx=526.0, cy=244.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.autumn.f5", prompt="", cx=545.0, cy=252.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.autumn.m5", prompt="", cx=560.0, cy=238.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.autumn.f6", prompt="", cx=578.0, cy=248.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.autumn.m6", prompt="", cx=592.0, cy=250.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.winter.f1", prompt="", cx=652.0, cy=220.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.winter.m1", prompt="", cx=669.0, cy=212.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.winter.f2", prompt="", cx=687.0, cy=226.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.winter.m2", prompt="", cx=703.0, cy=214.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.winter.f3", prompt="", cx=721.0, cy=228.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.winter.m3", prompt="", cx=736.0, cy=220.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.winter.f4", prompt="", cx=654.0, cy=248.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.winter.m4", prompt="", cx=672.0, cy=242.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.winter.f5", prompt="", cx=688.0, cy=250.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.winter.m5", prompt="", cx=706.0, cy=236.0, r=6.0, fill="#86D5EA"
            ),
            CircleSlot(
                id="slot.dot.winter.f6", prompt="", cx=722.0, cy=248.0, r=6.0, fill="#F29AB2"
            ),
            CircleSlot(
                id="slot.dot.winter.m6", prompt="", cx=738.0, cy=252.0, r=6.0, fill="#86D5EA"
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008887",
    "problem_type": "자료해석",
    "metadata": {
        "language": "ko",
        "question": "조사한 자료와 표 중에서 어느 것이 더 편리할까요?",
        "instruction": "자료의 종류를 비교하여 더 편리한 것을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.diagram", "type": "data_display", "label": "조사한 자료"},
            {"id": "obj.table", "type": "table", "label": "학생들이 태어난 계절"},
            {"id": "obj.seasons", "type": "category_set", "label": "봄, 여름, 가을, 겨울"},
            {"id": "obj.gender_counts", "type": "count_data", "label": "여학생 수와 남학생 수"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.diagram", "obj.table", "obj.seasons", "obj.gender_counts"],
                "target_ref": "answer.target",
                "condition_refs": [
                    "rel.table_represents_data",
                    "rel.table_groups_by_season_and_gender",
                ],
            },
            "plan": {
                "method": "compare_data_forms",
                "description": "같은 자료를 다른 방식으로 나타낸 것을 비교하여 더 편리한 자료를 판단한다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_display_forms",
                    "compare_readability",
                    "select_more_convenient_form",
                ]
            },
            "review": {
                "check_methods": ["information_accessibility_check", "same_data_consistency_check"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "more_convenient_display",
            "description": "조사한 자료와 표 중에서 더 편리한 것",
        },
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008887",
    "problem_type": "자료해석",
    "inputs": {
        "total_ticks": 0,
        "target_label": "더 편리한 것",
        "target_ticks": 0,
        "target_count": 0,
        "unit": "",
    },
    "given": [
        {"ref": "obj.diagram", "value": "조사한 자료"},
        {"ref": "obj.table", "value": "학생들이 태어난 계절"},
    ],
    "target": {"ref": "answer.target", "type": "more_convenient_display"},
    "method": "compare_data_forms",
    "plan": [
        "조사한 자료와 표가 같은 내용을 다른 방식으로 나타내는지 확인한다.",
        "여학생 수와 남학생 수를 한눈에 보기 쉬운 자료를 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "조사한 자료와 표를 비교한다",
            "value": "표가 더 직접적으로 수치를 확인하기 쉽다",
        }
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "표에는 계절별 여학생 수와 남학생 수가 정리되어 있는가",
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
            "type": "more_convenient_display",
            "description": "조사한 자료와 표 중에서 더 편리한 것",
        },
        "value": 0,
        "unit": "",
    },
}
