"""ModuMath Problem DSL: 각도기로 각도를 바르게 잰 것 선택하기 (S3_초등_4_007982)"""

from __future__ import annotations

import math

from modu_math.dsl import (
    Canvas,
    CircleSlot,
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
PROBLEM_ID = "S3_초등_4_007982"
PROBLEM_TITLE = "각도기로 각도를 바르게 잰 것 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "③",
    "answer_index": 2,
    "unit": "",
    "values": ["③"],
    "choices": [
        "①",
        "②",
        "③",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_2",
            "value": "③",
            "diagnostics": [
                {
                    "id": "diag.misaligned_baseline",
                    "condition": "answer_equals_1",
                    "concept": "각도기 사용법",
                    "reason": "각도기의 밑금이 아닌 맨 아래 테두리에 각의 한 변을 맞춘 그림을 선택함",
                    "feedback": "각도기의 중심을 각의 꼭짓점에 맞추고, 각도기의 밑금(0° 눈금선)을 각의 한 변에 맞추어야 합니다.",
                },
                {
                    "id": "diag.misaligned_center",
                    "condition": "answer_equals_2",
                    "concept": "각도기 사용법",
                    "reason": "각도기의 중심과 각의 꼭짓점이 어긋난 그림을 선택함",
                    "feedback": "각도기의 밑금은 맞추었지만, 각도기의 중심이 각의 꼭짓점과 어긋나 있습니다. 중심과 밑금을 모두 맞춘 ③이 바릅니다.",
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
    "problem_type": "multiple_choice_protractor_alignment",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "02단원_각도",
        "difficulty": "중",
    },
    "entities": {
        "option_0": {"label": "①", "center_aligned": True, "baseline_aligned": False},
        "option_1": {"label": "②", "center_aligned": False, "baseline_aligned": True},
        "option_2": {"label": "③", "center_aligned": True, "baseline_aligned": True},
    },
    "relations": [
        {
            "type": "correct_measurement_method",
            "correct_entity": "option_2",
            "distractors": ["option_0", "option_1"],
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
        text="90. 각도기로 각도를 바르게 잰 것을 선택하세요.",
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

    diagram_slots = []
    choice_cards = []
    centers = [166, 443, 720]
    labels = ["①", "②", "③"]
    # 각 꼭짓점 위치 (① 밑금 아래, ② 중심 오른쪽 어긋남, ③ 정위치)
    vertex_offsets = [(0, 12), (24, 0), (0, 0)]

    r_outer = 96
    for idx, (cx, label, (vx_off, vy_off)) in enumerate(zip(centers, labels, vertex_offsets)):
        cy = 218
        choice_cards.append(
            RectSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                x=cx - 122,
                y=84,
                width=244,
                height=178,
                fill="#ffffff",
                stroke="#e5e7eb",
                stroke_width=1.5,
                rx=10,
                ry=10,
                interaction={"type": "choice", "role": "answer", "choice_index": idx, "value": label, "group_id": "slot.choice.group", "include_in_submission": True},
            )
        )
        diagram_slots.append(TextSlot(id=f"slot.diagram.badge_{idx}", prompt="", text=label, x=cx - 102, y=98, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))
        diagram_slots.append(RectSlot(id=f"slot.diagram.pbase_{idx}", prompt="", x=cx - r_outer - 6, y=cy, width=(r_outer + 6) * 2, height=12, fill="#e0f2fe", stroke="#0284c7", stroke_width=1.2))
        diagram_slots.append(PathSlot(id=f"slot.diagram.parc_{idx}", prompt="", d=f"M {cx - r_outer} {cy} A {r_outer} {r_outer} 0 0 1 {cx + r_outer} {cy} Z", fill="#f0f9ff", stroke="#0284c7", stroke_width=1.4))
        diagram_slots.append(CircleSlot(id=f"slot.diagram.pcenter_{idx}", prompt="", cx=cx, cy=cy, r=2.5, fill="#0284c7", stroke="#0284c7", stroke_width=1))

        for deg in range(0, 181, 15):
            rad = math.radians(180 - deg)
            x1 = cx + r_outer * math.cos(rad)
            y1 = cy - r_outer * math.sin(rad)
            x2 = cx + (r_outer - 8) * math.cos(rad)
            y2 = cy - (r_outer - 8) * math.sin(rad)
            diagram_slots.append(LineSlot(id=f"slot.diagram.p{idx}_t_{deg}", prompt="", x1=round(x1, 1), y1=round(y1, 1), x2=round(x2, 1), y2=round(y2, 1), stroke="#0284c7", stroke_width=0.9))

        vx = cx + vx_off
        vy = cy + vy_off
        rad_50 = math.radians(50)
        rx = round(vx + 114 * math.cos(rad_50), 1)
        ry = round(vy - 114 * math.sin(rad_50), 1)
        diagram_slots.append(LineSlot(id=f"slot.diagram.ray_h_{idx}", prompt="", x1=vx, y1=vy, x2=vx + 116, y2=vy, stroke="#111827", stroke_width=2))
        diagram_slots.append(LineSlot(id=f"slot.diagram.ray_s_{idx}", prompt="", x1=vx, y1=vy, x2=rx, y2=ry, stroke="#111827", stroke_width=2))
        diagram_slots.append(PathSlot(id=f"slot.diagram.ang_arc_{idx}", prompt="", d=f"M {vx + 20} {vy} A 20 20 0 0 0 {round(vx + 20 * math.cos(rad_50), 1)} {round(vy - 20 * math.sin(rad_50), 1)}", fill="none", stroke="#ec4899", stroke_width=1.6))

    diagram_slot_ids = tuple(s.id for s in diagram_slots)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=290,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.option_0", "slot.choice.option_1", "slot.choice.option_2"),
            ),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=diagram_slot_ids),
        ),
        slots=(
            stem_text_slot,
            *choice_cards,
            *diagram_slots,
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
        {"ref": "option_0", "value": "밑금 불일치"},
        {"ref": "option_1", "value": "중심 불일치"},
        {"ref": "option_2", "value": "중심과 밑금 일치"},
    ],
    "target": {"ref": "slot.choice.option_2", "label": "바르게 잰 것", "unit": ""},
    "method": "protractor_alignment_check",
    "steps": [
        {
            "id": "verify_alignment",
            "expr": "③",
            "explanation": "각도기의 중심을 각의 꼭짓점에 맞추고, 각도기의 밑금을 각의 한 변에 맞춘 ③이 바릅니다.",
            "value": "③",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
