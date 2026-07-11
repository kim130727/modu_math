from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    CircleSlot,
    LineSlot,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "nested_semicircle_triangles_20260711"
PROBLEM_TITLE = "겹쳐진 반원과 삼각형"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=520,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=(
                    "slot.question",
                    "slot.instruction",
                ),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    # 아래에 있는 도형부터 먼저 그려집니다.
                    # 뒤쪽에 배치된 슬롯이 화면 위쪽에 표시됩니다.

                    # 삼각형
                    "slot.outer_triangle",
                    "slot.middle_triangle",
                    "slot.inner_triangle",

                    # 반원
                    "slot.outer_semicircle",
                    "slot.middle_semicircle",
                    "slot.inner_semicircle",

                    # 점선
                    "slot.left_dashed_line",
                    "slot.right_dashed_line",

                    # 중심점
                    "slot.center_point",
                ),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="vertical",
                slot_ids=("slot.answer",),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                text="그림을 보고 물음에 답하세요.",
                prompt="학생에게 제시할 문제 문장",
                semantic_role="question",
                x=48,
                y=32,
                width=804,
                height=54,
                font_size=28,
                line_height=1.35,
            ),
            TextBoxSlot(
                id="slot.instruction",
                text="겹쳐진 반원과 삼각형의 관계를 살펴보세요.",
                prompt="풀이 또는 응답 지시문",
                semantic_role="instruction",
                x=48,
                y=92,
                width=804,
                height=42,
                font_size=20,
                line_height=1.35,
            ),

            # =========================================================
            # 도형 영역
            #
            # 원본 좌표:
            # width=520, height=300
            #
            # DSL 캔버스 안에서 도형을 아래와 같이 이동합니다.
            # offset_x = 190
            # offset_y = 155
            #
            # 원본 중심점 (260, 267)
            # 실제 중심점 (450, 422)
            # =========================================================

            # ---------------------------------------------------------
            # 바깥쪽 삼각형
            # 원본:
            # (25, 267), (260, 32), (495, 267)
            # ---------------------------------------------------------
            PolygonSlot(
                id="slot.outer_triangle",
                prompt="가장 바깥쪽 회색 이등변삼각형",
                points=(
                    (215, 422),
                    (450, 187),
                    (685, 422),
                ),
                fill="#dddddd",
                stroke="#222222",
                stroke_width=2,
            ),

            # ---------------------------------------------------------
            # 가운데 삼각형
            # 원본:
            # (95, 267), (260, 102), (425, 267)
            # ---------------------------------------------------------
            PolygonSlot(
                id="slot.middle_triangle",
                prompt="가운데의 연한 회색 이등변삼각형",
                points=(
                    (285, 422),
                    (450, 257),
                    (615, 422),
                ),
                fill="#eeeeee",
                stroke="#222222",
                stroke_width=2,
            ),

            # ---------------------------------------------------------
            # 안쪽 삼각형
            # 원본:
            # (145, 267), (260, 152), (375, 267)
            # ---------------------------------------------------------
            PolygonSlot(
                id="slot.inner_triangle",
                prompt="가장 안쪽의 흰색 이등변삼각형",
                points=(
                    (335, 422),
                    (450, 307),
                    (565, 422),
                ),
                fill="#ffffff",
                stroke="#222222",
                stroke_width=2,
            ),

            # ---------------------------------------------------------
            # 바깥쪽 반원
            # 중심: (450, 422)
            # 반지름: 235
            #
            # 시작점: (215, 422)
            # 끝점:   (685, 422)
            # ---------------------------------------------------------
            PathSlot(
                id="slot.outer_semicircle",
                prompt="반지름이 235인 가장 바깥쪽 반원",
                d="M 215 422 A 235 235 0 0 1 685 422",
                fill="none",
                stroke="#222222",
                stroke_width=2,
            ),

            # ---------------------------------------------------------
            # 가운데 반원
            # 반지름: 165
            #
            # 시작점: (285, 422)
            # 끝점:   (615, 422)
            # ---------------------------------------------------------
            PathSlot(
                id="slot.middle_semicircle",
                prompt="반지름이 165인 가운데 반원",
                d="M 285 422 A 165 165 0 0 1 615 422",
                fill="none",
                stroke="#222222",
                stroke_width=2,
            ),

            # ---------------------------------------------------------
            # 안쪽 반원
            # 반지름: 115
            #
            # 시작점: (335, 422)
            # 끝점:   (565, 422)
            # ---------------------------------------------------------
            PathSlot(
                id="slot.inner_semicircle",
                prompt="반지름이 115인 가장 안쪽 반원",
                d="M 335 422 A 115 115 0 0 1 565 422",
                fill="none",
                stroke="#222222",
                stroke_width=2,
            ),

            # ---------------------------------------------------------
            # 왼쪽 점선
            # 원본:
            # (260, 267) → (178, 185)
            # ---------------------------------------------------------
            LineSlot(
                id="slot.left_dashed_line",
                prompt="중심점에서 왼쪽 위로 이어지는 점선",
                x1=450,
                y1=422,
                x2=368,
                y2=340,
                stroke="#222222",
                stroke_width=2,
                stroke_dasharray="8 7",
            ),

            # ---------------------------------------------------------
            # 오른쪽 점선
            # 원본:
            # (260, 267) → (342, 185)
            # ---------------------------------------------------------
            LineSlot(
                id="slot.right_dashed_line",
                prompt="중심점에서 오른쪽 위로 이어지는 점선",
                x1=450,
                y1=422,
                x2=532,
                y2=340,
                stroke="#222222",
                stroke_width=2,
                stroke_dasharray="8 7",
            ),

            # ---------------------------------------------------------
            # 공통 중심점
            # ---------------------------------------------------------
            CircleSlot(
                id="slot.center_point",
                prompt="세 반원의 공통 중심점",
                cx=450,
                cy=422,
                r=7,
                fill="#222222",
                stroke="none",
            ),

            BlankSlot(
                id="slot.answer",
                prompt="단답형 정답",
                answer_key="",
                placeholder="정답",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(
            "geometry",
            "semicircle",
            "triangle",
            "nested-shapes",
            "schema-compliant",
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
