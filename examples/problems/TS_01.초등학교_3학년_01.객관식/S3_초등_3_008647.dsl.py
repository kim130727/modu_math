from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    Region,
    TextSlot,
)


def _segment_fan_slots(prefix: str, *, cx: float, cy: float, r: float, label_top_only: bool = False):
    bottom = (cx, cy + r)
    points = {
        "a": (cx - r * 0.96, cy + r * 0.04),
        "b": (cx - r * 0.60, cy - r * 0.78),
        "c": (cx, cy - r),
        "d": (cx + r * 0.60, cy - r * 0.78),
        "e": (cx + r * 0.96, cy + r * 0.04),
    }
    labels = {
        "a": ("ㄱ", cx - r - 16, cy + 7),
        "b": ("ㄴ", cx - r * 0.93, cy - r * 0.70),
        "c": ("ㄷ", cx, cy - r - 18),
        "d": ("ㄹ", cx + r * 0.93, cy - r * 0.70),
        "e": ("ㅁ", cx + r + 16, cy + 7),
    }

    slots = [
        CircleSlot(
            id=f"{prefix}.circle",
            prompt="",
            cx=cx,
            cy=cy,
            r=r,
            fill="none",
            stroke="#222222",
            stroke_width=1.5,
        )
    ]
    for key, (x2, y2) in points.items():
        slots.append(
            LineSlot(
                id=f"{prefix}.segment.{key}",
                prompt="",
                x1=bottom[0],
                y1=bottom[1],
                x2=x2,
                y2=y2,
                stroke="#222222",
                stroke_width=1.5,
            )
        )

    slots.extend(
        [
            TextSlot(
                id=f"{prefix}.center.dot",
                prompt="",
                text="●",
                style_role="label",
                x=cx,
                y=cy + 4,
                font_size=12,
                anchor="middle",
                fill="#E11A86",
            ),
            TextSlot(
                id=f"{prefix}.center.label",
                prompt="",
                text="O",
                style_role="label",
                x=cx + 9,
                y=cy + 6,
                font_size=18,
            ),
        ]
    )

    label_keys = ("c",) if label_top_only else ("a", "b", "c", "d", "e")
    for key in label_keys:
        text, lx, ly = labels[key]
        slots.extend(
            [
                CircleSlot(
                    id=f"{prefix}.label.{key}.circle",
                    prompt="",
                    cx=lx,
                    cy=ly,
                    r=10.5,
                    fill="none",
                    stroke="#888888",
                    stroke_width=1.2,
                ),
                TextSlot(
                    id=f"{prefix}.label.{key}.text",
                    prompt="",
                    text=text,
                    style_role="label",
                    x=lx,
                    y=ly + 6,
                    font_size=17,
                    anchor="middle",
                    fill="#555555",
                ),
            ]
        )
    return tuple(slots)


def build_problem_template() -> ProblemTemplate:
    top_diagram = _segment_fan_slots("slot.diagram.top", cx=478.0, cy=185.0, r=96.0)
    solution_diagram = _segment_fan_slots("slot.diagram.solution", cx=195.0, cy=484.0, r=96.0, label_top_only=True)

    return ProblemTemplate(
        id="S3_초등_3_008647",
        title="원 안의 선분 중 길이가 가장 긴 선분 찾기",
        canvas=Canvas(width=960, height=360, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.no", "slot.q.text"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=tuple(slot.id for slot in top_diagram),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=("slot.answer",),
            ),
            Region(
                id="region.explanation",
                role="note",
                flow="absolute",
                slot_ids=(
                    "slot.explanation.label",
                    *(slot.id for slot in solution_diagram),
                    "slot.explanation.text1",
                    "slot.explanation.text2",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="원 안의 선분 중 길이가 가장 긴 선분을 찾아 기호를 선택하세요.",
                style_role="question",
                x=75.0,
                y=31.0,
                font_size=24,
            ),
            *top_diagram,
            ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("geometry", "circle", "diameter", "segment_comparison"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008647",
    "problem_type": "geometry_comparison",
    "metadata": {
        "language": "ko",
        "question": "원 안의 선분 중 길이가 가장 긴 선분을 찾아 기호를 선택하세요.",
        "instruction": "길이가 가장 긴 선분의 기호를 고른다.",
        "points": 5,
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.segment.c", "type": "segment", "symbol": "㉢", "role": "diameter"},
            {"id": "obj.center", "type": "point", "label": "O"},
        ],
        "relations": [
            {
                "id": "rel.segment_c_passes_center",
                "type": "incidence",
                "from_id": "obj.segment.c",
                "to_id": "obj.center",
                "description": "㉢ 선분은 원의 중심 O를 지난다.",
            },
            {
                "id": "rel.diameter_longest",
                "type": "circle_property",
                "from_id": "obj.segment.c",
                "to_id": "obj.circle",
                "description": "원 안에서 가장 긴 선분은 지름이다.",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.center"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.diameter_longest"],
            },
            "plan": {
                "method": "compare_segments_by_circle_property",
                "description": "원 안의 선분 중 중심을 지나는 지름을 찾는다.",
            },
            "execute": {"expected_operations": ["identify_center_passing_segment", "match_symbol_to_segment"]},
            "review": {"check_methods": ["property_check_longest_segment_is_diameter"]},
        },
    },
    "answer": {
        "type": "symbol_choice",
        "value": "㉢",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008647",
    "problem_type": "geometry_comparison",
    "inputs": {
        "target_label": "㉢",
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.segment.c", "value": {"symbol": "㉢", "property": "passes_through_center"}},
    ],
    "target": {"ref": "answer.target", "type": "symbol_choice"},
    "method": "compare_segments_by_circle_property",
    "plan": [
        "원 안의 선분 중 원의 중심 O를 지나는 선분을 찾는다.",
        "그 선분은 지름이므로 가장 긴 선분이다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "원의 중심 O를 지나는 선분 확인", "value": "㉢"},
        {"id": "step.2", "expr": "가장 긴 선분의 기호 선택", "value": "㉢"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "㉢은 원의 중심을 지나는 지름인가?",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "type": "symbol_choice",
        "value": "㉢",
        "unit": "",
    },
}
