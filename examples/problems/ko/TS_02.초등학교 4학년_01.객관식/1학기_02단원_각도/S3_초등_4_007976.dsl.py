"""ModuMath Problem DSL: 각도기의 바깥쪽 눈금 읽기 (S3_초등_4_007976)"""

from __future__ import annotations

import math

from modu_math.dsl import (
    Canvas,
    LineSlot,
    PathSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


# ==============================================================================
# 1. 문제 식별자 및 제목 (Problem Metadata)
# ==============================================================================
PROBLEM_ID = "S3_초등_4_007976"
PROBLEM_TITLE = "각도기의 바깥쪽 눈금을 읽어 각도 구하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "60°",
    "answer_index": 0,
    "unit": "°",
    "values": ["60°"],
    "choices": [
        "60°",
        "120°",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "60°",
            "diagnostics": [
                {
                    "id": "diag.read_inner_scale",
                    "condition": "answer_equals_120",
                    "concept": "각도기 눈금 읽기",
                    "reason": "바깥쪽 눈금 0에 맞추었으나 안쪽 눈금을 잘못 읽음",
                    "feedback": "각의 한 변이 바깥쪽 눈금 0에 맞춰져 있으므로 바깥쪽 눈금을 읽어야 합니다. 바깥쪽 눈금은 60°입니다.",
                },
            ],
        },
    ],
}


# ==============================================================================
# 3. 시맨틱 모델 정의 (Semantic Model & Metadata)
# ==============================================================================
SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_protractor_reading",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "02단원_각도",
        "difficulty": "하",
    },
    "entities": {
        "angle": {"label": "주어진 각", "value": 60, "unit": "°", "scale": "outer"},
    },
    "relations": [
        {
            "type": "measurement",
            "target": "angle",
            "value": "60°",
        }
    ],
}


# ==============================================================================
# 4. 문제 템플릿 빌더 (ProblemTemplate Builder)
# ==============================================================================
def build_problem_template() -> ProblemTemplate:
    """문제의 캔버스 크기, 슬롯(텍스트/도형/선택지), 리전(구역)을 정의합니다."""

    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="84. 각도를 읽으려고 합니다. 알맞은 것을 선택하세요.",
        x=32,
        y=24,
        width=820,
        height=44,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    cx, cy, r_outer, r_inner = 443, 214, 118, 86
    diagram_slots = [
        RectSlot(id="slot.diagram.prot_base", prompt="", x=cx - r_outer - 8, y=cy, width=(r_outer + 8) * 2, height=14, fill="#e0f2fe", stroke="#0284c7", stroke_width=1.2),
        PathSlot(id="slot.diagram.prot_arc", prompt="", d=f"M {cx - r_outer} {cy} A {r_outer} {r_outer} 0 0 1 {cx + r_outer} {cy} Z", fill="#f0f9ff", stroke="#0284c7", stroke_width=1.5),
        PathSlot(id="slot.diagram.prot_inner_arc", prompt="", d=f"M {cx - 28} {cy} A 28 28 0 0 1 {cx + 28} {cy}", fill="none", stroke="#38bdf8", stroke_width=1),
    ]

    for deg in range(0, 181, 10):
        rad = math.radians(180 - deg)
        x1 = cx + r_outer * math.cos(rad)
        y1 = cy - r_outer * math.sin(rad)
        x2 = cx + (r_outer - 10) * math.cos(rad)
        y2 = cy - (r_outer - 10) * math.sin(rad)
        diagram_slots.append(LineSlot(id=f"slot.diagram.tick_{deg}", prompt="", x1=round(x1, 1), y1=round(y1, 1), x2=round(x2, 1), y2=round(y2, 1), stroke="#0284c7", stroke_width=1))
        if deg % 30 == 0:
            lx = cx + (r_outer - 22) * math.cos(rad)
            ly = cy - (r_outer - 22) * math.sin(rad) - 6
            diagram_slots.append(TextSlot(id=f"slot.diagram.olabel_{deg}", prompt="", text=str(deg), x=round(lx, 1), y=round(ly, 1), font_size=11, font_family='"Noto Sans KR", sans-serif', fill="#0369a1", align="center"))
            ix = cx + (r_inner - 14) * math.cos(rad)
            iy = cy - (r_inner - 14) * math.sin(rad) - 5
            diagram_slots.append(TextSlot(id=f"slot.diagram.ilabel_{deg}", prompt="", text=str(180 - deg), x=round(ix, 1), y=round(iy, 1), font_size=10, font_family='"Noto Sans KR", sans-serif', fill="#0c4a6e", align="center"))

    # 각의 두 변 (바깥쪽 0°와 60°)
    rad_60 = math.radians(120)
    ray_x = round(cx + (r_outer + 18) * math.cos(rad_60), 1)
    ray_y = round(cy - (r_outer + 18) * math.sin(rad_60), 1)
    diagram_slots.extend([
        LineSlot(id="slot.diagram.ray_0", prompt="", x1=cx, y1=cy, x2=cx - r_outer - 18, y2=cy, stroke="#111827", stroke_width=2.2),
        LineSlot(id="slot.diagram.ray_60", prompt="", x1=cx, y1=cy, x2=ray_x, y2=ray_y, stroke="#111827", stroke_width=2.2),
        PathSlot(id="slot.diagram.angle_arc", prompt="", d=f"M {cx - 24} {cy} A 24 24 0 0 1 {round(cx + 24 * math.cos(rad_60), 1)} {round(cy - 24 * math.sin(rad_60), 1)}", fill="none", stroke="#ec4899", stroke_width=1.8),
        TextBoxSlot(
            id="slot.diagram.desc",
            prompt="",
            text="각의 한 변이 바깥쪽 눈금 0에 맞춰져 있으므로",
            x=120,
            y=244,
            width=646,
            height=34,
            font_size=21,
            font_family='"Noto Sans KR", sans-serif',
            fill="#111827",
            align="center",
            valign="middle",
        ),
    ])

    # 선택 영역: 바깥쪽 눈금을 읽으면 ( 60° , 120° )입니다.
    choice_prefix = TextSlot(id="slot.choice.prefix", prompt="", text="바깥쪽 눈금을 읽으면 (", x=290, y=288, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="60°",
        x=435,
        y=288,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "60°", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    comma = TextSlot(id="slot.choice.comma", prompt="", text=",", x=468, y=288, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="120°",
        x=508,
        y=288,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "120°", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    choice_suffix = TextSlot(id="slot.choice.suffix", prompt="", text=")입니다.", x=578, y=288, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    diagram_slot_ids = tuple(s.id for s in diagram_slots)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=345,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=diagram_slot_ids),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.prefix",
                    "slot.choice.option_0",
                    "slot.choice.comma",
                    "slot.choice.option_1",
                    "slot.choice.suffix",
                ),
            ),
        ),
        slots=(
            stem_text_slot,
            *diagram_slots,
            choice_prefix,
            choice_0,
            comma,
            choice_1,
            choice_suffix,
        ),
    )


# ==============================================================================
# 5. ModuMath 프레임워크 필수 익스포트
# ==============================================================================
PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = SEMANTIC
SEMANTIC_ANSWER = ANSWER
SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "problem_type": SEMANTIC["problem_type"],
    "given": [
        {"ref": "angle", "value": "바깥쪽 눈금 0에서 60", "unit": "°"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "각도", "unit": "°"},
    "method": "protractor_outer_scale_reading",
    "steps": [
        {
            "id": "read_outer_scale",
            "expr": "60°",
            "explanation": "각의 한 변이 바깥쪽 눈금 0에 맞춰져 있으므로 바깥쪽 눈금을 읽으면 60°입니다.",
            "value": "60°",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
