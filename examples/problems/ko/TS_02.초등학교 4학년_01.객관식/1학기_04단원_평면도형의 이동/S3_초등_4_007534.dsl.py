"""ModuMath Problem DSL: 한 직선에 수직인 두 직선의 관계 (S3_초등_4_007534)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    PathSlot,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
)


# ==============================================================================
# 1. 문제 식별자 및 제목 (Problem Metadata)
# ==============================================================================
PROBLEM_ID = "S3_초등_4_007534"
PROBLEM_TITLE = "한 직선에 수직인 두 직선의 평행 관계 알기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "평행합니다",
    "answer_index": 0,
    "unit": "",
    "values": ["평행합니다"],
    "choices": [
        "평행합니다",
        "수직입니다",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "평행합니다",
            "diagnostics": [
                {
                    "id": "diag.confused_parallel_perpendicular",
                    "condition": "answer_equals_perpendicular",
                    "concept": "평행선",
                    "reason": "한 직선에 수직인 두 직선의 관계를 수직으로 혼동함",
                    "feedback": "직선 가에 수직인 직선 나와 직선 다는 서로 만나지 않으므로 평행합니다.",
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
    "problem_type": "multiple_choice_parallel_lines_property",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "04단원_평면도형의 이동",
        "difficulty": "하",
    },
    "entities": {
        "line_ga": {"label": "가"},
        "line_na": {"label": "나"},
        "line_da": {"label": "다"},
    },
    "relations": [
        {"type": "perpendicular", "line1": "line_ga", "line2": "line_na"},
        {"type": "perpendicular", "line1": "line_ga", "line2": "line_da"},
        {"type": "parallel", "line1": "line_na", "line2": "line_da"},
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
        text="70. 삼각자를 사용하여 직선 가에 수직인 두 직선을 그었습니다. 알맞은 말을 선택하세요.",
        x=32,
        y=24,
        width=820,
        height=56,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    label_ga = TextSlot(id="slot.diagram.label_ga", prompt="", text="가", x=346, y=88, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    line_ga = LineSlot(id="slot.diagram.line_ga", prompt="", x1=346, y1=114, x2=346, y2=228, stroke="#111827", stroke_width=2)
    line_na = LineSlot(id="slot.diagram.line_na", prompt="", x1=346, y1=142, x2=546, y2=142, stroke="#111827", stroke_width=2)
    line_da = LineSlot(id="slot.diagram.line_da", prompt="", x1=346, y1=198, x2=546, y2=198, stroke="#111827", stroke_width=2)
    label_na = TextSlot(id="slot.diagram.label_na", prompt="", text="나", x=562, y=132, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    label_da = TextSlot(id="slot.diagram.label_da", prompt="", text="다", x=562, y=188, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    ra_na = PathSlot(id="slot.diagram.ra_na", prompt="", d="M 346 128 L 360 128 L 360 142", fill="none", stroke="#ec4899", stroke_width=1.5)
    ra_da = PathSlot(id="slot.diagram.ra_da", prompt="", d="M 346 184 L 360 184 L 360 198", fill="none", stroke="#ec4899", stroke_width=1.5)

    desc_text = TextBoxSlot(
        id="slot.diagram.desc_text",
        prompt="",
        text="→ 직선 가에 수직인 직선 나와 직선 다는 만나지 않으므로",
        x=80,
        y=236,
        width=726,
        height=34,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    prefix = TextSlot(id="slot.choice.prefix", prompt="", text="서로 (", x=286, y=282, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="평행합니다",
        x=386,
        y=282,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "평행합니다", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    comma = TextSlot(id="slot.choice.comma", prompt="", text=",", x=456, y=282, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="수직입니다",
        x=526,
        y=282,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "수직입니다", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    suffix = TextSlot(id="slot.choice.suffix", prompt="", text=").", x=602, y=282, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=340,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.label_ga",
                    "slot.diagram.line_ga",
                    "slot.diagram.line_na",
                    "slot.diagram.line_da",
                    "slot.diagram.label_na",
                    "slot.diagram.label_da",
                    "slot.diagram.ra_na",
                    "slot.diagram.ra_da",
                    "slot.diagram.desc_text",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.prefix", "slot.choice.option_0", "slot.choice.comma", "slot.choice.option_1", "slot.choice.suffix"),
            ),
        ),
        slots=(
            stem_text_slot,
            label_ga,
            line_ga,
            line_na,
            line_da,
            label_na,
            label_da,
            ra_na,
            ra_da,
            desc_text,
            prefix,
            choice_0,
            comma,
            choice_1,
            suffix,
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
        {"ref": "line_na", "value": "직선 가에 수직"},
        {"ref": "line_da", "value": "직선 가에 수직"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "직선 나와 직선 다의 관계", "unit": ""},
    "method": "parallel_lines_theorem",
    "steps": [
        {
            "id": "deduce_parallel",
            "expr": "나 // 다",
            "explanation": "직선 가에 수직인 직선 나와 직선 다는 만나지 않으므로 서로 평행합니다.",
            "value": "평행합니다",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
