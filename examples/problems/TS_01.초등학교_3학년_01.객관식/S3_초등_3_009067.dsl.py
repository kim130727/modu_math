from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot, LineSlot, PolygonSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_009067",
        title="도형을 보고 알맞은 기호를 모두 선택하기",
        canvas=Canvas(width=752, height=353, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qnum", "slot.qtext"),
            ),
            Region(
                id="region.top_diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.bg.top",
                    "slot.top.a",
                    "slot.top.b",
                    "slot.top.c",
                    "slot.top.d",
                    "slot.top.e",
                    "slot.top.la",
                    "slot.top.lb",
                    "slot.top.lc",
                    "slot.top.ld",
                    "slot.top.le",
                ),
            ),
            Region(
                id="region.statement", role="stem", flow="absolute", slot_ids=("slot.statement",)
            ),
            Region(id="region.answer", role="stem", flow="absolute", slot_ids=()),
            Region(
                id="region.explanation",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.bg.bottom",
                    "slot.bottom.a",
                    "slot.bottom.b",
                    "slot.bottom.c",
                    "slot.bottom.d",
                    "slot.bottom.e",
                    "slot.bottom.la",
                    "slot.bottom.lb",
                    "slot.bottom.lc",
                    "slot.bottom.ld",
                    "slot.bottom.le",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="8.",
                style_role="question",
                x=10.0,
                y=20.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="도형을 보고 알맞은 기호를 모두 선택하세요.",
                style_role="question",
                x=38.0,
                y=20.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.bg.top", prompt="", x=62.0, y=35.0, width=624.0, height=92.0, fill="none"
            ),
            PolygonSlot(
                id="slot.top.a",
                prompt="",
                points=((79.0, 54.0), (165.0, 54.0), (165.0, 117.0), (79.0, 117.0)),
                fill="none",
            ),
            PolygonSlot(
                id="slot.top.b",
                prompt="",
                points=((208.0, 54.0), (277.0, 54.0), (253.0, 117.0), (208.0, 117.0)),
                fill="none",
            ),
            PolygonSlot(
                id="slot.top.c",
                prompt="",
                points=((333.0, 54.0), (405.0, 54.0), (405.0, 117.0), (333.0, 117.0)),
                fill="none",
            ),
            PolygonSlot(
                id="slot.top.d",
                prompt="",
                points=((476.0, 54.0), (596.0, 54.0), (572.0, 117.0), (500.0, 117.0)),
                fill="none",
            ),
            PolygonSlot(
                id="slot.top.e",
                prompt="",
                points=((621.0, 38.0), (644.0, 89.0), (621.0, 128.0), (597.0, 89.0)),
                fill="none",
            ),
            TextSlot(
                id="slot.top.la",
                prompt="",
                text="가",
                style_role="label",
                x=127.0,
                y=97.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.top.lb",
                prompt="",
                text="나",
                style_role="label",
                x=237.0,
                y=97.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.top.lc",
                prompt="",
                text="다",
                style_role="label",
                x=368.0,
                y=97.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.top.ld",
                prompt="",
                text="라",
                style_role="label",
                x=538.0,
                y=97.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.top.le",
                prompt="",
                text="마",
                style_role="label",
                x=621.0,
                y=93.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.statement",
                prompt="",
                text="네 변의 길이가 모두 같은 사각형은 ( 가, 나, 다, 라, 마 )입니다.",
                style_role="question",
                x=62.0,
                y=162.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.bg.bottom",
                prompt="",
                x=62.0,
                y=211.0,
                width=494.0,
                height=92.0,
                fill="none",
            ),
            PolygonSlot(
                id="slot.bottom.a",
                prompt="",
                points=((79.0, 230.0), (165.0, 230.0), (165.0, 293.0), (79.0, 293.0)),
                fill="none",
            ),
            PolygonSlot(
                id="slot.bottom.b",
                prompt="",
                points=((208.0, 230.0), (277.0, 230.0), (253.0, 293.0), (208.0, 293.0)),
                fill="none",
            ),
            PolygonSlot(
                id="slot.bottom.c",
                prompt="",
                points=((333.0, 230.0), (405.0, 230.0), (405.0, 293.0), (333.0, 293.0)),
                fill="none",
            ),
            PolygonSlot(
                id="slot.bottom.d",
                prompt="",
                points=((476.0, 230.0), (596.0, 230.0), (572.0, 293.0), (500.0, 293.0)),
                fill="none",
            ),
            PolygonSlot(
                id="slot.bottom.e",
                prompt="",
                points=((621.0, 214.0), (644.0, 265.0), (621.0, 304.0), (597.0, 265.0)),
                fill="none",
            ),
            TextSlot(
                id="slot.bottom.la",
                prompt="",
                text="가",
                style_role="label",
                x=127.0,
                y=279.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bottom.lb",
                prompt="",
                text="나",
                style_role="label",
                x=237.0,
                y=279.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bottom.lc",
                prompt="",
                text="다",
                style_role="label",
                x=368.0,
                y=279.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bottom.ld",
                prompt="",
                text="라",
                style_role="label",
                x=538.0,
                y=279.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bottom.le",
                prompt="",
                text="마",
                style_role="label",
                x=621.0,
                y=275.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("도형", "사각형", "분류"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_009067",
    "problem_type": "도형 선택",
    "metadata": {
        "language": "ko",
        "question": "도형을 보고 알맞은 기호를 모두 선택하세요.",
        "instruction": "네 변의 길이가 모두 같은 사각형을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.shape.ga", "type": "quadrilateral", "label": "가"},
            {"id": "obj.shape.na", "type": "quadrilateral", "label": "나"},
            {"id": "obj.shape.da", "type": "quadrilateral", "label": "다"},
            {"id": "obj.shape.ra", "type": "quadrilateral", "label": "라"},
            {"id": "obj.shape.ma", "type": "quadrilateral", "label": "마"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.shape.ga",
                    "obj.shape.na",
                    "obj.shape.da",
                    "obj.shape.ra",
                    "obj.shape.ma",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.equal_sides_candidates"],
            },
            "plan": {
                "method": "shape_classification",
                "description": "네 변의 길이가 모두 같은 사각형인지 비교한다.",
            },
            "execute": {
                "expected_operations": [
                    "도형의 변 길이 성질을 확인한다",
                    "조건에 맞는 기호를 고른다",
                ]
            },
            "review": {"check_methods": ["조건과 선택한 기호가 일치하는지 확인한다"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_symbols",
            "description": "네 변의 길이가 모두 같은 사각형에 해당하는 기호",
        },
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009067",
    "problem_type": "도형 선택",
    "inputs": {
        "total_ticks": 5,
        "target_label": "네 변의 길이가 모두 같은 사각형",
        "target_ticks": 2,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.shape.ga", "value": {"label": "가"}},
        {"ref": "obj.shape.na", "value": {"label": "나"}},
        {"ref": "obj.shape.da", "value": {"label": "다"}},
        {"ref": "obj.shape.ra", "value": {"label": "라"}},
        {"ref": "obj.shape.ma", "value": {"label": "마"}},
    ],
    "plan": "도형의 네 변 길이 성질을 확인하여 조건에 맞는 기호를 고른다.",
    "steps": [
        {
            "id": "step.1",
            "expr": "문항의 조건 확인",
            "value": "네 변의 길이가 모두 같은 사각형을 찾는다",
        },
        {"id": "step.2", "expr": "보이는 정답 표기 확인", "value": "다, 마"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "정답 표기와 선택 기호가 일치하는가",
            "expected": "다, 마",
            "actual": "다, 마",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_symbols",
            "description": "네 변의 길이가 모두 같은 사각형에 해당하는 기호",
        },
        "value": 2,
        "unit": "",
    },
}
