"""ModuMath Problem DSL: 서로 평행한 변이 있는 도형 모두 선택하기 (S3_초등_4_007535)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


# ==============================================================================
# 1. 문제 식별자 및 제목 (Problem Metadata)
# ==============================================================================
PROBLEM_ID = "S3_초등_4_007535"
PROBLEM_TITLE = "서로 평행한 변이 있는 도형 모두 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": ["㉡", "㉢"],
    "unit": "",
    "values": ["㉡", "㉢"],
    "choices": [
        "㉠",
        "㉡",
        "㉢",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "㉡",
            "diagnostics": [
                {
                    "id": "diag.chose_triangle",
                    "condition": "answer_includes_giyeok",
                    "concept": "평행한 변",
                    "reason": "평행한 변이 없는 삼각형(㉠)을 선택함",
                    "feedback": "삼각형(㉠)에는 서로 평행한 변이 없습니다. 사다리꼴(㉡)과 직사각형(㉢)에 평행한 변이 있습니다.",
                },
            ],
        },
        {
            "slot_id": "slot.choice.option_2",
            "value": "㉢",
        },
    ],
}


# ==============================================================================
# 3. 시맨틱 모델 정의 (Semantic Model & Metadata)
# ==============================================================================
SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_parallel_sides",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "04단원_평면도형의 이동",
        "difficulty": "하",
    },
    "entities": {
        "shape_0": {"label": "㉠", "type": "triangle", "has_parallel_sides": False},
        "shape_1": {"label": "㉡", "type": "trapezoid", "has_parallel_sides": True},
        "shape_2": {"label": "㉢", "type": "rectangle", "has_parallel_sides": True},
    },
    "relations": [
        {
            "type": "has_parallel_sides",
            "correct_entities": ["shape_1", "shape_2"],
            "distractor": "shape_0",
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
        text="71. 서로 평행한 변이 있는 도형을 모두 선택해 보세요.",
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

    outer_box = RectSlot(id="slot.diagram.outer_box", prompt="", x=116, y=82, width=730, height=174, fill="#ffffff", stroke="#8b5cf6", stroke_width=1.6)

    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="㉠",
        x=152,
        y=102,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "㉠", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    poly_0 = PolygonSlot(id="slot.diagram.poly_0", prompt="", points=[(184, 226), (330, 226), (274, 108)], fill="none", stroke="#111827", stroke_width=2)

    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="㉡",
        x=402,
        y=102,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "㉡", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    poly_1 = PolygonSlot(id="slot.diagram.poly_1", prompt="", points=[(476, 118), (566, 118), (608, 222), (434, 222)], fill="none", stroke="#111827", stroke_width=2)

    choice_2 = TextSlot(
        id="slot.choice.option_2",
        prompt="",
        text="㉢",
        x=672,
        y=102,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "㉢", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    poly_2 = RectSlot(id="slot.diagram.poly_2", prompt="", x=706, y=108, width=106, height=114, fill="none", stroke="#111827", stroke_width=2)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=280,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=("slot.diagram.outer_box", "slot.diagram.poly_0", "slot.diagram.poly_1", "slot.diagram.poly_2")),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1", "slot.choice.option_2")),
        ),
        slots=(
            stem_text_slot,
            outer_box,
            choice_0,
            poly_0,
            choice_1,
            poly_1,
            choice_2,
            poly_2,
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
        {"ref": "shape_0", "value": "삼각형"},
        {"ref": "shape_1", "value": "사다리꼴"},
        {"ref": "shape_2", "value": "직사각형"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "평행한 변이 있는 도형", "unit": ""},
    "method": "parallel_sides_identification",
    "steps": [
        {
            "id": "find_parallel_shapes",
            "expr": "㉡, ㉢",
            "explanation": "사다리꼴(㉡)은 위·아래 변이 평행하고, 직사각형(㉢)은 마주 보는 두 쌍의 변이 평행합니다.",
            "value": ["㉡", "㉢"],
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
