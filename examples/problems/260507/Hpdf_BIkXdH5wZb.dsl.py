from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_BIkXdH5wZb",
        title="시계가 9시 정각을 가리키고 있습니다",
        canvas=Canvas(width=905, height=324, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q3", "slot.q4"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="시계가 9시 정각을 가리키고 있습니다. 지금부",
                style_role="question",
                x=16.0,
                y=40.0,
                font_size=35,
                anchor="start",
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="터 2시간 동안 긴바늘과 짧은바늘이 이루는 작",
                style_role="question",
                x=16.0,
                y=100.0,
                font_size=35,
                anchor="start",
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="은 쪽의 각이 직각인 시각은 모두 몇 번 있습니",
                style_role="question",
                x=16.0,
                y=160.0,
                font_size=35,
                anchor="start",
            ),
            TextSlot(
                id="slot.q4",
                prompt="",
                text="까?",
                style_role="question",
                x=16.0,
                y=220.0,
                font_size=35,
                anchor="start",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_BIkXdH5wZb",
    "problem_type": "clock_angle_count",
    "metadata": {
        "language": "ko",
        "question": "시계가 9시 정각을 가리키고 있습니다. 지금부터 2시간 동안 긴바늘과 짧은바늘이 이루는 작은 쪽의 각이 직각인 시각은 모두 몇 번 있습니까?",
        "instruction": "",
    },
    "domain": {
        "objects": [
            {"id": "obj.clock", "type": "clock"},
            {"id": "obj.start_time", "type": "time", "hour": 9, "minute": 0},
            {"id": "obj.duration", "type": "duration", "hour": 2},
            {"id": "obj.hand.minute", "type": "hand", "name": "긴바늘"},
            {"id": "obj.hand.hour", "type": "hand", "name": "짧은바늘"},
            {
                "id": "obj.condition",
                "type": "angle_condition",
                "relation": "small_angle_is_right_angle",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.start_time",
                    "obj.duration",
                    "obj.hand.minute",
                    "obj.hand.hour",
                    "obj.condition",
                ],
                "target_ref": "answer.target",
                "condition_refs": [],
            },
            "plan": {
                "method": "clock_angle_counting",
                "description": "시작 시각부터 2시간 동안 작은 쪽의 각이 직각이 되는 시각의 개수를 센다.",
            },
            "execute": {
                "expected_operations": ["시간구간해석", "조건판별", "개수세기"]
            },
            "review": {"check_methods": ["조건일치확인", "구간포함확인"]},
        },
    },
    "answer": {
        "target": {
            "type": "count",
            "description": "지금부터 2시간 동안 긴바늘과 짧은바늘이 이루는 작은 쪽의 각이 직각인 시각의 수",
        },
        "value": 4,
        "unit": "번",
    },
}
SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "Hpdf_BIkXdH5wZb",
    "problem_type": "clock_angle_count",
    "inputs": {
        "total_ticks": 0,
        "target_label": "직각인 시각의 수",
        "target_ticks": 0,
        "target_count": 0,
        "unit": "번",
    },
    "given": [
        {"ref": "obj.start_time", "value": {"hour": 9, "minute": 0}},
        {"ref": "obj.duration", "value": {"hour": 2}},
    ],
    "target": {"ref": "answer.target", "type": "count"},
    "method": "clock_angle_counting",
    "plan": [
        "9시 정각부터 2시간 동안(9:00~11:00) 직각이 되는 시각을 찾는다.",
        "9:00 정각에 직각이 된다.",
        "9시와 10시 사이에 한 번 더 직각이 된다.",
        "10시와 11시 사이에 두 번 직각이 된다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "operation": "count_times",
            "expr": "1 (9:00) + 1 (9시 대) + 2 (10시 대)",
            "value": 4,
        }
    ],
    "checks": [
        {
            "id": "check.1",
            "type": "interval_check",
            "expr": "구간 해석이 9:00~11:00인지 확인",
            "expected": 1,
            "actual": 1,
            "pass": True,
        }
    ],
    "answer": {"value": 4, "unit": "번", "derived_from": "step.1"},
}
