"""ModuMath Problem DSL: 각도기를 사용하여 수선 그은 것 선택하기 (S3_초등_4_007533)"""

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
PROBLEM_ID = "S3_초등_4_007533"
PROBLEM_TITLE = "각도기를 사용하여 주어진 직선에 대한 수선을 그은 것 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "①",
    "answer_index": 0,
    "unit": "",
    "values": ["①"],
    "choices": [
        "①",
        "②",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "①",
            "diagnostics": [
                {
                    "id": "diag.not_90_degrees",
                    "condition": "answer_equals_2",
                    "concept": "각도기로 수선 긋기",
                    "reason": "90°가 아닌 눈금(60°/120°)에 맞춰 그은 그림(②)을 선택함",
                    "feedback": "주어진 직선에 각도기의 밑금을 맞추고 90°가 되는 눈금에 점을 찍어 이은 ①이 수선입니다.",
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
    "problem_type": "multiple_choice_perpendicular_construction",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "04단원_평면도형의 이동",
        "difficulty": "하",
    },
    "entities": {
        "option_0": {"label": "①", "angle_deg": 90, "is_perpendicular": True},
        "option_1": {"label": "②", "angle_deg": 60, "is_perpendicular": False},
    },
    "relations": [
        {
            "type": "correct_construction",
            "correct_entity": "option_0",
            "distractor": "option_1",
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
        text="69. 각도기를 사용하여 주어진 직선에 대한 수선을 그은 것을 선택하세요.",
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
    centers = [280, 606]
    labels = ["①", "②"]
    ray_angles = [90, 62]  # 각도기 기준 각도
    tilt = 18  # 반시계 기울기(도)
    r_outer = 96

    for idx, (cx, label, ray_deg) in enumerate(zip(centers, labels, ray_angles)):
        cy = 218
        choice_cards.append(
            RectSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                x=cx - 144,
                y=84,
                width=288,
                height=188,
                fill="#ffffff",
                stroke="#a78bfa",
                stroke_width=1.5,
                rx=12,
                ry=12,
                interaction={"type": "choice", "role": "answer", "choice_index": idx, "value": label, "group_id": "slot.choice.group", "include_in_submission": True},
            )
        )
        diagram_slots.append(TextSlot(id=f"slot.diagram.badge_{idx}", prompt="", text=label, x=cx - 122, y=98, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))

        # 기울어진 각도기 밑선 양끝
        t_rad = math.radians(tilt)
        lx = cx - (r_outer + 18) * math.cos(t_rad)
        ly = cy + (r_outer + 18) * math.sin(t_rad)
        rx = cx + (r_outer + 18) * math.cos(t_rad)
        ry = cy - (r_outer + 18) * math.sin(t_rad)
        diagram_slots.append(LineSlot(id=f"slot.diagram.base_{idx}", prompt="", x1=round(lx, 1), y1=round(ly, 1), x2=round(rx, 1), y2=round(ry, 1), stroke="#111827", stroke_width=2))

        ax1 = cx - r_outer * math.cos(t_rad)
        ay1 = cy + r_outer * math.sin(t_rad)
        ax2 = cx + r_outer * math.cos(t_rad)
        ay2 = cy - r_outer * math.sin(t_rad)
        diagram_slots.append(
            PathSlot(
                id=f"slot.diagram.parc_{idx}",
                prompt="",
                d=f"M {round(ax1, 1)} {round(ay1, 1)} A {r_outer} {r_outer} 0 0 1 {round(ax2, 1)} {round(ay2, 1)} Z",
                fill="#f0f9ff",
                stroke="#0284c7",
                stroke_width=1.4,
            )
        )

        for deg in range(0, 181, 15):
            rad = math.radians(deg + tilt)
            tx1 = cx + r_outer * math.cos(rad)
            ty1 = cy - r_outer * math.sin(rad)
            tx2 = cx + (r_outer - 8) * math.cos(rad)
            ty2 = cy - (r_outer - 8) * math.sin(rad)
            diagram_slots.append(LineSlot(id=f"slot.diagram.p{idx}_t_{deg}", prompt="", x1=round(tx1, 1), y1=round(ty1, 1), x2=round(tx2, 1), y2=round(ty2, 1), stroke="#0284c7", stroke_width=0.9))

        r_rad = math.radians(ray_deg + tilt)
        diagram_slots.append(
            LineSlot(
                id=f"slot.diagram.ray_{idx}",
                prompt="",
                x1=cx,
                y1=cy,
                x2=round(cx + (r_outer + 16) * math.cos(r_rad), 1),
                y2=round(cy - (r_outer + 16) * math.sin(r_rad), 1),
                stroke="#111827",
                stroke_width=2,
            )
        )

    diagram_slot_ids = tuple(s.id for s in diagram_slots)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=300,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
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
        {"ref": "option_0", "value": "90° 눈금에 맞춘 직선"},
        {"ref": "option_1", "value": "62° 눈금에 맞춘 직선"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "수선을 바르게 그은 것", "unit": ""},
    "method": "protractor_90_degree_check",
    "steps": [
        {
            "id": "verify_90_deg",
            "expr": "①",
            "explanation": "각도기의 중심과 밑금을 직선에 맞추고 90° 눈금에 맞춰 그린 ①이 수선입니다.",
            "value": "①",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
