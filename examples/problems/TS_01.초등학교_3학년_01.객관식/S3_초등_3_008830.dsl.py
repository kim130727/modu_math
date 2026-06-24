from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    LineSlot,
    PathSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008830",
        title="알맞은 물건 고르기",
        canvas=Canvas(width=940, height=540, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q.title",
                    "slot.box.border",
                    "slot.box.title",
                    "slot.item1.img",
                    "slot.item1.label",
                    "slot.item2.img",
                    "slot.item2.label",
                    "slot.item3.img",
                    "slot.item3.label",
                    "slot.sentence",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.title",
                prompt="",
                text="66. <보기를 보고 알맞은 물건을 선택하여 문장을 완성해 보세요.",
                style_role="question",
                x=10.0,
                y=28.0,
                font_size=28,
            ),
            RectSlot(id="slot.box.border", prompt="", x=100.0, y=48.0, width=760.0, height=226.0),
            TextSlot(
                id="slot.box.title",
                prompt="",
                text="<보기>",
                style_role="label",
                x=120.0,
                y=82.0,
                font_size=28,
            ),
            PathSlot(
                id="slot.item1.img",
                prompt="",
                d="M 200.0 155.0 C 215.0 148.0, 228.0 145.0, 236.0 144.0 C 245.0 143.0, 252.0 145.0, 259.0 150.0 L 244.0 159.0 C 235.0 164.0, 228.0 168.0, 219.0 171.0 L 208.0 175.0 C 204.0 176.0, 201.0 175.0, 198.0 173.0 L 192.0 169.0 L 184.0 173.0 L 177.0 165.0 L 184.0 160.0 L 177.0 155.0 L 192.0 150.0 Z",
            ),
            PathSlot(
                id="slot.item1.img2",
                prompt="",
                d="M 208.0 159.0 C 208.0 153.0, 209.0 149.0, 214.0 146.0 C 219.0 143.0, 226.0 143.0, 231.0 146.0",
            ),
            TextSlot(
                id="slot.item1.label",
                prompt="",
                text="주사기",
                style_role="label",
                x=194.0,
                y=236.0,
                font_size=28,
            ),
            PathSlot(
                id="slot.item2.img",
                prompt="",
                d="M 454.0 160.0 C 468.0 144.0, 487.0 141.0, 503.0 148.0 C 509.0 150.0, 515.0 156.0, 520.0 163.0 L 520.0 176.0 C 520.0 181.0, 516.0 185.0, 511.0 185.0 L 446.0 185.0 C 441.0 185.0, 437.0 181.0, 437.0 176.0 L 437.0 167.0 C 440.0 163.0, 445.0 161.0, 454.0 160.0 Z",
            ),
            PathSlot(
                id="slot.item2.img2",
                prompt="",
                d="M 472.0 149.0 C 470.0 132.0, 482.0 120.0, 491.0 120.0 C 500.0 120.0, 504.0 128.0, 504.0 137.0",
            ),
            PathSlot(
                id="slot.item2.img3",
                prompt="",
                d="M 520.0 164.0 C 541.0 157.0, 551.0 163.0, 551.0 174.0 C 551.0 185.0, 541.0 192.0, 528.0 187.0",
            ),
            TextSlot(
                id="slot.item2.label",
                prompt="",
                text="물뿌리개",
                style_role="label",
                x=442.0,
                y=236.0,
                font_size=28,
            ),
            PathSlot(
                id="slot.item3.img",
                prompt="",
                d="M 681.0 145.0 C 689.0 132.0, 708.0 126.0, 725.0 129.0 C 742.0 132.0, 754.0 145.0, 759.0 163.0 C 763.0 177.0, 762.0 194.0, 754.0 208.0 C 749.0 218.0, 739.0 224.0, 727.0 226.0 C 707.0 228.0, 689.0 222.0, 679.0 210.0 C 670.0 199.0, 667.0 183.0, 670.0 168.0 C 672.0 159.0, 675.0 151.0, 681.0 145.0 Z",
            ),
            PathSlot(
                id="slot.item3.img2",
                prompt="",
                d="M 693.0 137.0 C 699.0 130.0, 709.0 127.0, 720.0 127.0 C 731.0 127.0, 741.0 131.0, 747.0 138.0",
            ),
            PathSlot(
                id="slot.item3.img3",
                prompt="",
                d="M 679.0 153.0 C 694.0 148.0, 710.0 146.0, 728.0 146.0 C 744.0 146.0, 754.0 150.0, 761.0 157.0",
            ),
            TextSlot(
                id="slot.item3.label",
                prompt="",
                text="항아리",
                style_role="label",
                x=683.0,
                y=236.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.sentence",
                prompt="",
                text="( 주사기 , 물뿌리개 , 항아리 )의 들이는 약 3 mL입니다.",
                style_role="question",
                x=148.0,
                y=347.0,
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
    "problem_id": "S3_초등_3_008830",
    "problem_type": "선택형_들이_단위",
    "metadata": {
        "language": "ko",
        "question": "보기의 물건 중 약 3 mL의 들이에 알맞은 물건을 고르는 문제",
        "instruction": "보기에서 알맞은 물건을 선택하여 문장을 완성한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.syringe", "type": "object", "name": "주사기"},
            {"id": "obj.watering_can", "type": "object", "name": "물뿌리개"},
            {"id": "obj.jar", "type": "object", "name": "항아리"},
            {"id": "obj.volume", "type": "volume", "value": 3, "unit": "mL"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.syringe", "obj.watering_can", "obj.jar", "obj.volume"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.match_volume"],
            },
            "plan": {
                "method": "compare_scale",
                "description": "보기의 물건들 중 약 3 mL와 어울리는 작은 들이의 물건을 고른다.",
            },
            "execute": {
                "expected_operations": ["compare_object_capacity", "select_small_volume_object"]
            },
            "review": {"check_methods": ["unit_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_object", "description": "약 3 mL의 들이에 알맞은 물건"},
        "value": "주사기",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008830",
    "problem_type": "선택형_들이_단위",
    "inputs": {
        "total_ticks": 1,
        "target_label": "약 3 mL의 들이에 알맞은 물건",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "mL",
    },
    "given": [
        {"ref": "obj.syringe", "value": {"name": "주사기"}},
        {"ref": "obj.watering_can", "value": {"name": "물뿌리개"}},
        {"ref": "obj.jar", "value": {"name": "항아리"}},
        {"ref": "obj.volume", "value": {"value": 3, "unit": "mL"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_object"},
    "method": "compare_scale",
    "plan": ["보기의 물건들 중 약 3 mL와 가장 잘 맞는 작은 들이의 물건을 고른다."],
    "steps": [
        {
            "id": "step.1",
            "expr": "주사기, 물뿌리개, 항아리 중 약 3 mL에 알맞은 물건을 비교한다.",
            "value": "주사기",
        }
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "작은 들이의 물건인가?",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_object", "description": "약 3 mL의 들이에 알맞은 물건"},
        "value": "주사기",
        "unit": "",
    },
}
