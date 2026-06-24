from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008822",
        title="들이가 많은 컵 순서 고르기",
        canvas=Canvas(width=960, height=420, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.water_bottle",
                    "slot.table_outer",
                    "slot.table_hdr",
                    "slot.table_row_label",
                    "slot.table_c1",
                    "slot.table_c2",
                    "slot.table_c3",
                    "slot.table_v1",
                    "slot.table_v2",
                    "slot.table_v3",
                ),
            ),
            Region(
                id="region.options",
                role="options",
                flow="absolute",
                slot_ids=("slot.opt1", "slot.opt2", "slot.opt3", "slot.opt4"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 56. 물통에 물을 가득 채우기 위해 ㉠ 컵, ㉡ 컵, ㉢ 컵으로 물을 같은 간격 부어야 합니다. 들이가 많은 컵부터 순서대로 쓴 것을 고르세요.",
                style_role="question",
                x=18.0,
                y=42.0,
                font_size=28,
            ),
            RectSlot(id="slot.water_bottle", prompt="", x=52.0, y=112.0, width=56.0, height=96.0),
            RectSlot(id="slot.table_outer", prompt="", x=255.0, y=112.0, width=606.0, height=86.0),
            RectSlot(id="slot.table_hdr", prompt="", x=255.0, y=112.0, width=606.0, height=40.0),
            TextSlot(
                id="slot.table_row_label",
                prompt="",
                text="컵의 수",
                style_role="body",
                x=292.0,
                y=173.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table_c1",
                prompt="",
                text="㉠ 컵",
                style_role="body",
                x=396.0,
                y=146.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table_c2",
                prompt="",
                text="㉡ 컵",
                style_role="body",
                x=540.0,
                y=146.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table_c3",
                prompt="",
                text="㉢ 컵",
                style_role="body",
                x=694.0,
                y=146.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table_v1",
                prompt="",
                text="3개",
                style_role="body",
                x=401.0,
                y=193.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table_v2",
                prompt="",
                text="9개",
                style_role="body",
                x=547.0,
                y=193.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table_v3",
                prompt="",
                text="5개",
                style_role="body",
                x=701.0,
                y=193.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt1",
                prompt="",
                text="① ㉠ 컵, ㉡ 컵, ㉢ 컵",
                style_role="body",
                x=34.0,
                y=258.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt2",
                prompt="",
                text="② ㉠ 컵, ㉢ 컵, ㉡ 컵",
                style_role="body",
                x=518.0,
                y=258.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt3",
                prompt="",
                text="③ ㉡ 컵, ㉢ 컵, ㉠ 컵",
                style_role="body",
                x=34.0,
                y=310.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt4",
                prompt="",
                text="④ ㉢ 컵, ㉡ 컵, ㉠ 컵",
                style_role="body",
                x=518.0,
                y=310.0,
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
    "problem_id": "S3_초등_3_008822",
    "problem_type": "choice_ordering",
    "metadata": {
        "language": "ko",
        "question": "들이가 많은 컵부터 순서대로 고르는 문제",
        "instruction": "보기에서 알맞은 순서를 고르기",
    },
    "domain": {
        "objects": [
            {"id": "obj.cup_a", "type": "cup", "label": "㉠ 컵"},
            {"id": "obj.cup_b", "type": "cup", "label": "㉡ 컵"},
            {"id": "obj.cup_c", "type": "cup", "label": "㉢ 컵"},
            {"id": "obj.container", "type": "container", "label": "물통"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.cup_a", "obj.cup_b", "obj.cup_c", "rel.cup_count_to_capacity"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.cup_count_to_capacity"],
            },
            "plan": {
                "method": "compare_counts",
                "description": "물통을 채우는 데 필요한 컵 수의 상대적 크기를 보고 들이의 순서를 판단한다.",
            },
            "execute": {
                "expected_operations": ["compare cup counts", "order by inverse capacity relation"]
            },
            "review": {"check_methods": ["count_inverse_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "ordered_choice", "description": "들이가 많은 컵부터 순서대로"},
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008822",
    "problem_type": "choice_ordering",
    "inputs": {
        "total_ticks": 1,
        "target_label": "들이가 많은 컵부터 순서대로",
        "target_ticks": 1,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {"ref": "obj.cup_a", "value": {"label": "㉠ 컵", "count": 3}},
        {"ref": "obj.cup_b", "value": {"label": "㉡ 컵", "count": 9}},
        {"ref": "obj.cup_c", "value": {"label": "㉢ 컵", "count": 5}},
    ],
    "target": {"ref": "answer.target", "type": "ordered_choice"},
    "method": "inverse_relation_ordering",
    "plan": [
        "같은 물통을 채우는 데 필요한 컵 수를 비교한다.",
        "컵 수가 적을수록 들이가 많으므로, 적은 순서로 나열한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "㉠: 3개, ㉡: 9개, ㉢: 5개",
            "value": {"order_by_count_asc": ["㉠ 컵", "㉢ 컵", "㉡ 컵"]},
        }
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "컵의 수가 적을수록 들이가 많다",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "ordered_choice", "description": "들이가 많은 컵부터 순서대로"},
        "value": 2,
        "unit": "",
    },
}
