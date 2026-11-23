"""ModuMath Problem DSL: 막대그래프와 꺾은선그래프의 같은 점 (S3_초등_4_007711)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


# ==============================================================================
# 1. 문제 식별자 및 제목 (Problem Metadata)
# ==============================================================================
PROBLEM_ID = "S3_초등_4_007711"
PROBLEM_TITLE = "막대그래프와 꺾은선그래프의 가로, 세로, 눈금 한 칸 값 찾기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": ["월", "무게", "1"],
    "unit": "",
    "values": ["월", "무게", "1"],
    "choices": [
        "월",
        "무게",
        "1",
        "10",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.g1_option_0",
            "value": "월",
            "diagnostics": [
                {
                    "id": "diag.swapped_horizontal_axis",
                    "condition": "answer_equals_weight",
                    "concept": "그래프의 가로와 세로",
                    "reason": "가로축(월)과 세로축(무게)을 반대로 선택함",
                    "feedback": "그래프의 가로에는 조사한 '월'(8, 9, 10, 11)이, 세로에는 '무게'(kg)가 나타나 있습니다.",
                },
            ],
        },
        {
            "slot_id": "slot.choice.g2_option_1",
            "value": "무게",
        },
        {
            "slot_id": "slot.choice.g3_option_0",
            "value": "1",
            "diagnostics": [
                {
                    "id": "diag.wrong_unit_scale",
                    "condition": "answer_equals_10",
                    "concept": "세로 눈금 한 칸의 크기",
                    "reason": "5칸이 5 kg임을 1칸이 10 kg인 것으로 오인함",
                    "feedback": "세로 눈금 5칸이 5 kg을 나타내므로, 세로 눈금 한 칸은 1 kg을 나타냅니다.",
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
    "problem_type": "multiple_choice_chart_comparison",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "05단원_막대그래프",
        "difficulty": "하",
    },
    "entities": {
        "horizontal_axis": {"label": "가로", "value": "월"},
        "vertical_axis": {"label": "세로", "value": "무게"},
        "unit_scale": {"label": "세로 눈금 한 칸", "value": 1, "unit": "kg"},
    },
    "relations": [
        {
            "type": "chart_axis_mapping",
            "horizontal": "월",
            "vertical": "무게",
            "tick_step": 1,
        }
    ],
}


# ==============================================================================
# 4. 문제 템플릿 빌더 (ProblemTemplate Builder)
# ==============================================================================
def _build_goat_charts() -> list:
    slots = []
    # 왼쪽: 막대그래프 (x=76..396, y=104..268)
    slots.append(TextSlot(id="slot.diagram.t_left", prompt="", text="염소의 무게", x=236, y=82, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    slots.append(RectSlot(id="slot.diagram.bg_l_y", prompt="", x=76, y=104, width=82, height=130, fill="#d1fae5", stroke="#6b7280", stroke_width=1))
    slots.append(RectSlot(id="slot.diagram.bg_l_x", prompt="", x=158, y=234, width=238, height=34, fill="#d1fae5", stroke="#6b7280", stroke_width=1))
    slots.append(RectSlot(id="slot.diagram.bg_l_c", prompt="", x=76, y=234, width=82, height=34, fill="#d1fae5", stroke="#6b7280", stroke_width=1))
    slots.append(LineSlot(id="slot.diagram.diag_l", prompt="", x1=76, y1=268, x2=158, y2=234, stroke="#6b7280", stroke_width=1))
    slots.append(TextSlot(id="slot.diagram.l_unit", prompt="", text="(kg)", x=100, y=112, font_size=13, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    slots.append(TextSlot(id="slot.diagram.l_wy", prompt="", text="무게", x=96, y=240, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    slots.append(TextSlot(id="slot.diagram.l_wx", prompt="", text="월", x=138, y=250, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    for v in range(0, 21, 5):
        gy = round(234 - (v / 20) * 120, 1)
        slots.append(LineSlot(id=f"slot.diagram.l_grid_{v}", prompt="", x1=158, y1=gy, x2=396, y2=gy, stroke="#9ca3af", stroke_width=0.9))
        slots.append(TextSlot(id=f"slot.diagram.l_ylbl_{v}", prompt="", text=str(v), x=146, y=gy - 6, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="end"))

    months = ["8", "9", "10", "11"]
    vals = [8, 10, 14, 20]
    for i, (m, val) in enumerate(zip(months, vals)):
        cx = 188 + i * 58
        bh = round((val / 20) * 120, 1)
        slots.append(RectSlot(id=f"slot.diagram.l_bar_{i}", prompt="", x=cx - 12, y=round(234 - bh, 1), width=24, height=bh, fill="#fed7aa", stroke="#f97316", stroke_width=1.2))
        slots.append(TextSlot(id=f"slot.diagram.l_xlbl_{i}", prompt="", text=m, x=cx, y=244, font_size=13, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    # 오른쪽: 꺾은선그래프 (x=470..810, y=104..268)
    slots.append(TextSlot(id="slot.diagram.t_right", prompt="", text="염소의 무게", x=640, y=82, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    slots.append(RectSlot(id="slot.diagram.bg_r_y", prompt="", x=470, y=104, width=82, height=130, fill="#d1fae5", stroke="#6b7280", stroke_width=1))
    slots.append(RectSlot(id="slot.diagram.bg_r_x", prompt="", x=552, y=234, width=258, height=34, fill="#d1fae5", stroke="#6b7280", stroke_width=1))
    slots.append(RectSlot(id="slot.diagram.bg_r_c", prompt="", x=470, y=234, width=82, height=34, fill="#d1fae5", stroke="#6b7280", stroke_width=1))
    slots.append(LineSlot(id="slot.diagram.diag_r", prompt="", x1=470, y1=268, x2=552, y2=234, stroke="#6b7280", stroke_width=1))
    slots.append(TextSlot(id="slot.diagram.r_unit", prompt="", text="(kg)", x=494, y=112, font_size=13, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    slots.append(TextSlot(id="slot.diagram.r_wy", prompt="", text="무게", x=490, y=240, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    slots.append(TextSlot(id="slot.diagram.r_wx", prompt="", text="월", x=532, y=250, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    for v in range(0, 21, 5):
        gy = round(234 - (v / 20) * 120, 1)
        slots.append(LineSlot(id=f"slot.diagram.r_grid_{v}", prompt="", x1=552, y1=gy, x2=810, y2=gy, stroke="#9ca3af", stroke_width=0.9))
        slots.append(TextSlot(id=f"slot.diagram.r_ylbl_{v}", prompt="", text=str(v), x=540, y=gy - 6, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="end"))

    pts = []
    for i, (m, val) in enumerate(zip(months, vals)):
        px = 596 + i * 52
        py = round(234 - (val / 20) * 120, 1)
        pts.append((px, py))
        slots.append(LineSlot(id=f"slot.diagram.r_vgrid_{i}", prompt="", x1=px, y1=104, x2=px, y2=234, stroke="#9ca3af", stroke_width=0.9))
        slots.append(TextSlot(id=f"slot.diagram.r_xlbl_{i}", prompt="", text=m, x=px, y=240, font_size=13, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    for i in range(len(pts) - 1):
        slots.append(LineSlot(id=f"slot.diagram.r_seg_{i}", prompt="", x1=pts[i][0], y1=pts[i][1], x2=pts[i + 1][0], y2=pts[i + 1][1], stroke="#ec4899", stroke_width=2))
    for i, (px, py) in enumerate(pts):
        slots.append(CircleSlot(id=f"slot.diagram.r_dot_{i}", prompt="", cx=px, cy=py, r=3, fill="#111827", stroke="#111827", stroke_width=1))

    return slots


def build_problem_template() -> ProblemTemplate:
    """문제의 캔버스 크기, 슬롯(텍스트/도형/선택지), 리전(구역)을 정의합니다."""

    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="100. 염소의 무게를 매월 1일에 조사하여 나타낸 막대그래프와 꺾은선그래프입니다. 두 그래프의 같은 점을 알아보고 알맞은 것을 선택하세요.",
        x=32,
        y=20,
        width=820,
        height=52,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.45,
    )

    diagram_slots = _build_goat_charts()

    # (1) 가로는 ( 월 , 무게 )을/를 나타내고, 세로는 ( 월 , 무게 )을/를 나타냅니다.
    q1_pre = TextSlot(id="slot.choice.q1_pre", prompt="", text="(1) 가로는 (", x=116, y=286, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g1_0 = TextSlot(id="slot.choice.g1_option_0", prompt="", text="월", x=196, y=286, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "월", "group_id": "slot.choice.group_1", "include_in_submission": True})
    g1_c = TextSlot(id="slot.choice.g1_c", prompt="", text=",", x=218, y=286, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g1_1 = TextSlot(id="slot.choice.g1_option_1", prompt="", text="무게", x=250, y=286, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "무게", "group_id": "slot.choice.group_1", "include_in_submission": True})
    q1_mid = TextSlot(id="slot.choice.q1_mid", prompt="", text=")을/를 나타내고, 세로는 (", x=390, y=286, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g2_0 = TextSlot(id="slot.choice.g2_option_0", prompt="", text="월", x=516, y=286, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "월", "group_id": "slot.choice.group_2", "include_in_submission": True})
    g2_c = TextSlot(id="slot.choice.g2_c", prompt="", text=",", x=538, y=286, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g2_1 = TextSlot(id="slot.choice.g2_option_1", prompt="", text="무게", x=570, y=286, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "무게", "group_id": "slot.choice.group_2", "include_in_submission": True})
    q1_suf = TextSlot(id="slot.choice.q1_suf", prompt="", text=")을/를 나타냅니다.", x=686, y=286, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    # (2) 세로 눈금 한 칸은 ( 1 , 10 ) kg을 나타냅니다.
    q2_pre = TextSlot(id="slot.choice.q2_pre", prompt="", text="(2) 세로 눈금 한 칸은 (", x=156, y=326, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g3_0 = TextSlot(id="slot.choice.g3_option_0", prompt="", text="1", x=278, y=326, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "1", "group_id": "slot.choice.group_3", "include_in_submission": True})
    g3_c = TextSlot(id="slot.choice.g3_c", prompt="", text=",", x=298, y=326, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g3_1 = TextSlot(id="slot.choice.g3_option_1", prompt="", text="10", x=324, y=326, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "10", "group_id": "slot.choice.group_3", "include_in_submission": True})
    q2_suf = TextSlot(id="slot.choice.q2_suf", prompt="", text=") kg을 나타냅니다.", x=436, y=326, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    choice_slots = (q1_pre, g1_0, g1_c, g1_1, q1_mid, g2_0, g2_c, g2_1, q1_suf, q2_pre, g3_0, g3_c, g3_1, q2_suf)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=376,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=tuple(s.id for s in choice_slots)),
        ),
        slots=(
            stem_text_slot,
            *diagram_slots,
            *choice_slots,
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
        {"ref": "horizontal_axis", "value": "월"},
        {"ref": "vertical_axis", "value": "무게"},
    ],
    "target": {"ref": "slot.choice.g3_option_0", "label": "가로, 세로, 눈금 한 칸", "unit": ""},
    "method": "chart_structure_reading",
    "steps": [
        {
            "id": "read_axes_and_scale",
            "expr": "(1) 월, 무게 (2) 1",
            "explanation": "가로는 월, 세로는 무게를 나타내며 세로 눈금 한 칸은 1 kg입니다.",
            "value": ["월", "무게", "1"],
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
