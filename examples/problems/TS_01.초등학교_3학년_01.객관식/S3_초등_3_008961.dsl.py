from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008961",
        title="학생들의 혈액형 그림그래프",
        canvas=Canvas(width=946, height=699, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1", "slot.q2")),
            Region(
                id="region.table",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.table.title",
                    "slot.table.outer",
                    "slot.table.head",
                    "slot.table.vline",
                    "slot.table.h1",
                    "slot.table.h2",
                    "slot.table.h3",
                    "slot.table.h4",
                    "slot.table.row.a",
                    "slot.table.row.b",
                    "slot.table.row.ab",
                    "slot.table.row.o",
                    "slot.table.label.a",
                    "slot.table.label.b",
                    "slot.table.label.ab",
                    "slot.table.label.o",
                    "slot.icon.a.big1",
                    "slot.icon.a.big2",
                    "slot.icon.a.big3",
                    "slot.icon.a.small1",
                    "slot.icon.a.small2",
                    "slot.icon.a.small3",
                    "slot.icon.a.small4",
                    "slot.icon.a.small5",
                    "slot.icon.b.big1",
                    "slot.icon.b.big2",
                    "slot.icon.b.small1",
                    "slot.icon.b.small2",
                    "slot.icon.b.small3",
                    "slot.icon.b.small4",
                    "slot.icon.b.small5",
                    "slot.icon.b.small6",
                    "slot.icon.b.small7",
                    "slot.icon.b.small8",
                    "slot.icon.b.small9",
                    "slot.icon.b.small10",
                    "slot.icon.ab.big1",
                    "slot.icon.ab.big2",
                    "slot.icon.ab.small1",
                    "slot.icon.ab.small2",
                    "slot.icon.ab.small3",
                    "slot.icon.ab.small4",
                    "slot.icon.ab.small5",
                    "slot.icon.ab.small6",
                    "slot.icon.ab.small7",
                    "slot.icon.o.big1",
                    "slot.icon.o.big2",
                    "slot.icon.o.big3",
                    "slot.icon.o.small1",
                    "slot.icon.o.small2",
                    "slot.icon.o.small3",
                    "slot.icon.o.small4",
                    "slot.legend.big",
                    "slot.legend.big_text",
                    "slot.legend.small",
                    "slot.legend.small_text",
                ),
            ),
            Region(
                id="region.choices",
                role="answer_choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.1",
                    "slot.choice.2",
                    "slot.choice.3",
                    "slot.choice.4",
                    "slot.choice.5",
                ),
            ),
            Region(id="region.explanation", role="explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 31. 정호네 학교 학생 1250명의 혈액형을 조사하여 그림그래프로 나타내었습니다.",
                style_role="question",
                x=16.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="학생 수가 많은 혈액형부터 차례대로 나타낸 것을 고르세요.",
                style_role="question",
                x=16.0,
                y=68.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.title",
                prompt="",
                text="학생들의 혈액형",
                style_role="title",
                x=372.0,
                y=125.0,
                font_size=28,
            ),
            RectSlot(id="slot.table.outer", prompt="", x=266.0, y=172.0, width=400.0, height=217.0),
            RectSlot(id="slot.table.head", prompt="", x=266.0, y=172.0, width=400.0, height=46.0),
            RectSlot(id="slot.table.vline", prompt="", x=355.0, y=172.0, width=1.0, height=217.0),
            RectSlot(id="slot.table.h1", prompt="", x=266.0, y=218.0, width=400.0, height=1.0),
            RectSlot(id="slot.table.h2", prompt="", x=266.0, y=260.0, width=400.0, height=1.0),
            RectSlot(id="slot.table.h3", prompt="", x=266.0, y=302.0, width=400.0, height=1.0),
            RectSlot(id="slot.table.h4", prompt="", x=266.0, y=344.0, width=400.0, height=1.0),
            RectSlot(id="slot.table.row.a", prompt="", x=266.0, y=218.0, width=400.0, height=42.0),
            RectSlot(id="slot.table.row.b", prompt="", x=266.0, y=260.0, width=400.0, height=42.0),
            RectSlot(id="slot.table.row.ab", prompt="", x=266.0, y=302.0, width=400.0, height=42.0),
            RectSlot(id="slot.table.row.o", prompt="", x=266.0, y=344.0, width=400.0, height=45.0),
            TextSlot(
                id="slot.table.label.a",
                prompt="",
                text="A",
                style_role="label",
                x=304.0,
                y=248.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.label.b",
                prompt="",
                text="B",
                style_role="label",
                x=304.0,
                y=290.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.label.ab",
                prompt="",
                text="AB",
                style_role="label",
                x=299.0,
                y=332.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.label.o",
                prompt="",
                text="O",
                style_role="label",
                x=304.0,
                y=376.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.icon.a.big1", prompt="", cx=378.0, cy=237.0, r=11.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.a.big2", prompt="", cx=408.0, cy=237.0, r=11.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.a.big3", prompt="", cx=438.0, cy=237.0, r=11.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.a.small1", prompt="", cx=468.0, cy=237.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.a.small2", prompt="", cx=486.0, cy=237.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.a.small3", prompt="", cx=504.0, cy=237.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.a.small4", prompt="", cx=522.0, cy=237.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.a.small5", prompt="", cx=540.0, cy=237.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.b.big1", prompt="", cx=378.0, cy=279.0, r=11.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.b.big2", prompt="", cx=408.0, cy=279.0, r=11.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.b.small1", prompt="", cx=438.0, cy=279.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.b.small2", prompt="", cx=456.0, cy=279.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.b.small3", prompt="", cx=474.0, cy=279.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.b.small4", prompt="", cx=492.0, cy=279.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.b.small5", prompt="", cx=510.0, cy=279.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.b.small6", prompt="", cx=528.0, cy=279.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.b.small7", prompt="", cx=546.0, cy=279.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.b.small8", prompt="", cx=564.0, cy=279.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.b.small9", prompt="", cx=582.0, cy=279.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.b.small10", prompt="", cx=600.0, cy=279.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.ab.big1", prompt="", cx=378.0, cy=321.0, r=11.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.ab.big2", prompt="", cx=408.0, cy=321.0, r=11.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.ab.small1", prompt="", cx=438.0, cy=321.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.ab.small2", prompt="", cx=456.0, cy=321.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.ab.small3", prompt="", cx=474.0, cy=321.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.ab.small4", prompt="", cx=492.0, cy=321.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.ab.small5", prompt="", cx=510.0, cy=321.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.ab.small6", prompt="", cx=528.0, cy=321.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.ab.small7", prompt="", cx=546.0, cy=321.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.ab.small8", prompt="", cx=564.0, cy=321.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.o.big1", prompt="", cx=378.0, cy=363.0, r=11.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.o.big2", prompt="", cx=408.0, cy=363.0, r=11.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.o.big3", prompt="", cx=438.0, cy=363.0, r=11.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.o.small1", prompt="", cx=468.0, cy=363.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.o.small2", prompt="", cx=486.0, cy=363.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.o.small3", prompt="", cx=504.0, cy=363.0, r=6.0, fill="#F7D94C"
            ),
            CircleSlot(
                id="slot.icon.o.small4", prompt="", cx=522.0, cy=363.0, r=6.0, fill="#F7D94C"
            ),
            TextSlot(
                id="slot.legend.big",
                prompt="",
                text="🙂",
                style_role="label",
                x=540.0,
                y=432.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.legend.big_text",
                prompt="",
                text="100명",
                style_role="label",
                x=568.0,
                y=432.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.legend.small",
                prompt="",
                text="◦",
                style_role="label",
                x=632.0,
                y=432.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.legend.small_text",
                prompt="",
                text="10명",
                style_role="label",
                x=650.0,
                y=432.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="① A, B, O, AB",
                style_role="choice",
                x=36.0,
                y=513.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text="② AB, O, B, A",
                style_role="choice",
                x=344.0,
                y=513.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.3",
                prompt="",
                text="③ A, O, B, AB",
                style_role="choice",
                x=648.0,
                y=513.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.4",
                prompt="",
                text="④ O, A, B, AB",
                style_role="choice",
                x=36.0,
                y=555.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.5",
                prompt="",
                text="⑤ B, O, A, AB",
                style_role="choice",
                x=344.0,
                y=555.0,
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
    "problem_id": "S3_초등_3_008961",
    "problem_type": "ordering_from_pictograph",
    "metadata": {
        "language": "ko",
        "question": "정호네 학교 학생 1250명의 혈액형을 조사하여 그림그래프로 나타내었습니다. 학생 수가 많은 혈액형부터 차례대로 나타낸 것을 고르세요.",
        "instruction": "보기에서 학생 수가 많은 혈액형부터 순서대로 고르기",
    },
    "domain": {
        "objects": [
            {"id": "obj.blood_type.A", "type": "blood_type", "name": "A형"},
            {"id": "obj.blood_type.B", "type": "blood_type", "name": "B형"},
            {"id": "obj.blood_type.AB", "type": "blood_type", "name": "AB형"},
            {"id": "obj.blood_type.O", "type": "blood_type", "name": "O형"},
            {
                "id": "obj.legend.big",
                "type": "pictograph_symbol",
                "name": "큰 얼굴",
                "quantity_per_symbol": 100,
            },
            {
                "id": "obj.legend.small",
                "type": "pictograph_symbol",
                "name": "작은 얼굴",
                "quantity_per_symbol": 10,
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.legend.big",
                    "obj.legend.small",
                    "obj.blood_type.A",
                    "obj.blood_type.B",
                    "obj.blood_type.AB",
                    "obj.blood_type.O",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare.counts"],
            },
            "plan": {
                "method": "compare_pictograph_counts",
                "description": "그림그래프에서 각 혈액형의 기호 개수를 비교해 학생 수가 많은 순서를 찾는다.",
            },
            "execute": {
                "expected_operations": ["compare_symbol_counts", "determine_descending_order"]
            },
            "review": {"check_methods": ["order_matches_pictograph"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "descending_order_of_blood_types",
            "description": "학생 수가 많은 혈액형부터 차례대로 나열한 보기",
        },
        "value": 3,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008961",
    "problem_type": "ordering_from_pictograph",
    "inputs": {
        "total_ticks": 1250,
        "target_label": "혈액형 순서",
        "target_ticks": 4,
        "target_count": 4,
        "unit": "혈액형",
    },
    "given": [
        {"ref": "obj.legend.big", "value": {"quantity_per_symbol": 100}},
        {"ref": "obj.legend.small", "value": {"quantity_per_symbol": 10}},
        {"ref": "obj.blood_type.A", "value": {"name": "A형"}},
        {"ref": "obj.blood_type.B", "value": {"name": "B형"}},
        {"ref": "obj.blood_type.AB", "value": {"name": "AB형"}},
        {"ref": "obj.blood_type.O", "value": {"name": "O형"}},
    ],
    "target": {"ref": "answer.target", "type": "descending_order_of_blood_types"},
    "method": "compare_pictograph_counts",
    "plan": ["그림그래프의 기호 개수를 비교하여 각 혈액형의 학생 수가 많은 순서를 찾는다."],
    "steps": [
        {
            "id": "step.1",
            "expr": "A형, B형, AB형, O형의 기호 개수 비교",
            "value": "A형과 O형이 B형과 AB형보다 많음",
        },
        {
            "id": "step.2",
            "expr": "학생 수가 많은 순서 정리",
            "value": ["A형", "O형", "B형", "AB형"],
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "보기 ③이 학생 수가 많은 혈액형부터의 순서와 일치하는가",
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
            "type": "descending_order_of_blood_types",
            "description": "학생 수가 많은 혈액형부터 차례대로 나열한 보기",
        },
        "value": 3,
        "unit": "",
    },
}
