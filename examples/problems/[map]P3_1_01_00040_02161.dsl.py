from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    CircleSlot,
    Group,
    LineSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)

PROBLEM_ID = "P3_1_01_00040_02161"
PROBLEM_TITLE = "문방구를 들러 학교까지 간 거리"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=650,
            height=240,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=("slot.instruction",),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    # 송은이네 집
                    "slot.house_body",
                    "slot.house_roof",
                    "slot.house_door",
                    "slot.house_window",
                    "slot.house_chimney",
                    "slot.house_label",
                    "slot.point_home",
                    # 문방구
                    "slot.store_body",
                    "slot.store_sign",
                    "slot.store_awning",
                    "slot.store_door",
                    "slot.store_window",
                    "slot.store_label",
                    "slot.point_store",
                    # 학교
                    "slot.school_body",
                    "slot.school_roof",
                    "slot.school_door",
                    "slot.school_window_1",
                    "slot.school_window_2",
                    "slot.school_label",
                    "slot.point_school",
                    # 거리 경로
                    "slot.route_home_store",
                    "slot.route_store_school",
                    "slot.distance_487",
                    "slot.distance_295",
                    # 풀이 입력 영역
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.instruction",
                text="송은이가 문방구를 들러 학교에 가려고 합니다. 집에서 학교까지의 거리를 구하시오.",
                prompt="문방구를 거쳐 학교까지 간 전체 거리를 구하라는 문제",
                semantic_role="instruction",
                x=20,
                y=8,
                width=610,
                height=52,
                font_size=18,
                line_height=1.2,
                fill="#111111",
                align="left",
            ),
            # ---------------------------------------------------------
            # 송은이네 집
            # ---------------------------------------------------------
            RectSlot(
                id="slot.house_body",
                prompt="송은이네 집 건물",
                x=42,
                y=64,
                width=42,
                height=34,
                fill="#E9A068",
                stroke="#B46F44",
                stroke_width=1.5,
            ),
            PolygonSlot(
                id="slot.house_roof",
                prompt="송은이네 집 지붕",
                points=((34, 67), (63, 45), (92, 67)),
                fill="#D9674E",
                stroke="#B94E3C",
                stroke_width=1.5,
            ),
            RectSlot(
                id="slot.house_door",
                prompt="송은이네 집 문",
                x=58,
                y=78,
                width=11,
                height=20,
                fill="#8B5A3C",
                stroke="#6E442E",
                stroke_width=1,
            ),
            RectSlot(
                id="slot.house_window",
                prompt="송은이네 집 창문",
                x=74,
                y=73,
                width=9,
                height=9,
                fill="#BFE5F7",
                stroke="#5D91A8",
                stroke_width=1,
            ),
            RectSlot(
                id="slot.house_chimney",
                prompt="송은이네 집 굴뚝",
                x=66,
                y=43,
                width=6,
                height=11,
                fill="#9B4B3C",
                stroke="#7A372E",
                stroke_width=1,
            ),
            TextSlot(
                id="slot.house_label",
                text="송은이네 집",
                prompt="출발 장소 이름",
                x=24,
                y=116,
                font_size=14,
                anchor="start",
                fill="#444444",
            ),
            CircleSlot(
                id="slot.point_home",
                prompt="집 위치를 나타내는 점",
                cx=87,
                cy=83,
                r=3,
                fill="#7A4A35",
                stroke="#7A4A35",
                stroke_width=1,
            ),
            # ---------------------------------------------------------
            # 문방구
            # ---------------------------------------------------------
            RectSlot(
                id="slot.store_body",
                prompt="문방구 건물",
                x=226,
                y=47,
                width=50,
                height=56,
                fill="#D8EEF4",
                stroke="#6C929E",
                stroke_width=1.5,
            ),
            RectSlot(
                id="slot.store_sign",
                prompt="문방구 간판",
                x=229,
                y=50,
                width=44,
                height=15,
                fill="#F5E6CB",
                stroke="#B68E58",
                stroke_width=1,
            ),
            PolygonSlot(
                id="slot.store_awning",
                prompt="문방구 차양",
                points=((229, 66), (273, 66), (268, 76), (234, 76)),
                fill="#E56E6E",
                stroke="#B94E4E",
                stroke_width=1,
            ),
            RectSlot(
                id="slot.store_door",
                prompt="문방구 문",
                x=252,
                y=77,
                width=17,
                height=26,
                fill="#8EC4D5",
                stroke="#5E93A2",
                stroke_width=1,
            ),
            RectSlot(
                id="slot.store_window",
                prompt="문방구 창문",
                x=232,
                y=78,
                width=15,
                height=15,
                fill="#BDE5F2",
                stroke="#5E93A2",
                stroke_width=1,
            ),
            TextSlot(
                id="slot.store_label",
                text="문방구",
                prompt="중간 장소 이름",
                x=283,
                y=86,
                font_size=14,
                anchor="start",
                fill="#444444",
            ),
            CircleSlot(
                id="slot.point_store",
                prompt="문방구 위치를 나타내는 점",
                cx=232,
                cy=93,
                r=3,
                fill="#7A4A35",
                stroke="#7A4A35",
                stroke_width=1,
            ),
            # ---------------------------------------------------------
            # 학교
            # ---------------------------------------------------------
            RectSlot(
                id="slot.school_body",
                prompt="학교 건물",
                x=248,
                y=156,
                width=49,
                height=37,
                fill="#F4D37A",
                stroke="#B79A4E",
                stroke_width=1.5,
            ),
            PolygonSlot(
                id="slot.school_roof",
                prompt="학교 지붕",
                points=((242, 158), (272, 139), (303, 158)),
                fill="#8FC487",
                stroke="#62975A",
                stroke_width=1.5,
            ),
            RectSlot(
                id="slot.school_door",
                prompt="학교 출입문",
                x=266,
                y=174,
                width=13,
                height=19,
                fill="#8AB8C8",
                stroke="#5C8998",
                stroke_width=1,
            ),
            RectSlot(
                id="slot.school_window_1",
                prompt="학교 왼쪽 창문",
                x=253,
                y=164,
                width=8,
                height=8,
                fill="#BFE5F7",
                stroke="#5D91A8",
                stroke_width=1,
            ),
            RectSlot(
                id="slot.school_window_2",
                prompt="학교 오른쪽 창문",
                x=284,
                y=164,
                width=8,
                height=8,
                fill="#BFE5F7",
                stroke="#5D91A8",
                stroke_width=1,
            ),
            TextSlot(
                id="slot.school_label",
                text="학교",
                prompt="도착 장소 이름",
                x=305,
                y=187,
                font_size=14,
                anchor="start",
                fill="#444444",
            ),
            CircleSlot(
                id="slot.point_school",
                prompt="학교 위치를 나타내는 점",
                cx=268,
                cy=143,
                r=3,
                fill="#7A4A35",
                stroke="#7A4A35",
                stroke_width=1,
            ),
            # ---------------------------------------------------------
            # 이동 경로와 거리
            # ---------------------------------------------------------
            LineSlot(
                id="slot.route_home_store",
                prompt="집에서 문방구까지의 이동 경로",
                x1=87,
                y1=83,
                x2=232,
                y2=93,
                stroke="#8A6A58",
                stroke_width=1.5,
            ),
            LineSlot(
                id="slot.route_store_school",
                prompt="문방구에서 학교까지의 이동 경로",
                x1=232,
                y1=93,
                x2=268,
                y2=143,
                stroke="#8A6A58",
                stroke_width=2,
            ),
            TextSlot(
                id="slot.distance_487",
                text="487 m",
                prompt="집에서 문방구까지의 거리 487미터",
                x=157,
                y=73,
                font_size=16,
                anchor="middle",
                fill="#222222",
            ),
            TextSlot(
                id="slot.distance_295",
                text="295 m",
                prompt="문방구에서 학교까지의 거리 295미터",
                x=272,
                y=118,
                font_size=16,
                anchor="middle",
                fill="#222222",
            ),
            # ---------------------------------------------------------
            # 식과 답
            # ---------------------------------------------------------
            BlankSlot(
                id="slot.expression_blank",
                prompt="집에서 학교까지의 거리를 구하는 식",
                answer_key="487 + 295 = 782",
                placeholder="",
            ),
            BlankSlot(
                id="slot.answer_blank",
                prompt="집에서 학교까지의 전체 거리",
                answer_key="782",
                placeholder="",
            ),
        ),
        diagrams=(),
        groups=(
            Group(
                id="group.home",
                role="place_home",
                member_ids=(
                    "slot.house_body",
                    "slot.house_roof",
                    "slot.house_door",
                    "slot.house_window",
                    "slot.house_chimney",
                    "slot.house_label",
                    "slot.point_home",
                ),
            ),
            Group(
                id="group.store",
                role="place_stationery_store",
                member_ids=(
                    "slot.store_body",
                    "slot.store_sign",
                    "slot.store_awning",
                    "slot.store_door",
                    "slot.store_window",
                    "slot.store_label",
                    "slot.point_store",
                ),
            ),
            Group(
                id="group.school",
                role="place_school",
                member_ids=(
                    "slot.school_body",
                    "slot.school_roof",
                    "slot.school_door",
                    "slot.school_window_1",
                    "slot.school_window_2",
                    "slot.school_label",
                    "slot.point_school",
                ),
            ),
            Group(
                id="group.route",
                role="two_segment_route",
                member_ids=(
                    "slot.route_home_store",
                    "slot.route_store_school",
                    "slot.distance_487",
                    "slot.distance_295",
                ),
            ),
        ),
        constraints=(),
        tags=(
            "grade-3",
            "addition",
            "three-digit-addition",
            "distance",
            "route",
            "word-problem",
            "numeric-answer",
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_route_distance_addition",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": (
            "송은이가 문방구를 들러 학교에 가려고 합니다. " "집에서 학교까지의 거리를 구하시오."
        ),
    },
    "domain": {
        "objects": [
            {
                "id": "person.songeun",
                "type": "person",
                "label": "송은이",
            },
            {
                "id": "place.home",
                "type": "place",
                "label": "송은이네 집",
            },
            {
                "id": "place.stationery_store",
                "type": "place",
                "label": "문방구",
            },
            {
                "id": "place.school",
                "type": "place",
                "label": "학교",
            },
            {
                "id": "route.home_to_store",
                "type": "route_segment",
                "label": "집에서 문방구까지의 길",
            },
            {
                "id": "route.store_to_school",
                "type": "route_segment",
                "label": "문방구에서 학교까지의 길",
            },
        ],
        "relations": [
            {
                "id": "relation.distance_home_store",
                "type": "distance",
                "from_id": "place.home",
                "to_id": "place.stationery_store",
                "value": 487,
                "unit": "m",
            },
            {
                "id": "relation.distance_store_school",
                "type": "distance",
                "from_id": "place.stationery_store",
                "to_id": "place.school",
                "value": 295,
                "unit": "m",
            },
            {
                "id": "relation.total_distance",
                "type": "sum",
                "from_ids": [
                    "relation.distance_home_store",
                    "relation.distance_store_school",
                ],
                "to_id": "answer.total_distance",
                "equation": "487 + 295 = 782",
            },
        ],
    },
    "answer": {
        "blanks": [
            {
                "id": "slot.expression_blank",
                "type": "expression",
                "value": "487 + 295 = 782",
            },
            {
                "id": "slot.answer_blank",
                "type": "number",
                "value": 782,
                "unit": "m",
            },
        ],
        "choices": [],
        "answer_key": [
            {
                "blank_id": "slot.expression_blank",
                "value": "487 + 295 = 782",
            },
            {
                "blank_id": "slot.answer_blank",
                "value": 782,
                "unit": "m",
            },
        ],
    },
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_route_distance_addition",
    "inputs": {
        "target_label": "집에서 문방구를 거쳐 학교까지 간 전체 거리",
        "unit": "m",
        "quantities": {
            "home_to_store_distance": 487,
            "store_to_school_distance": 295,
        },
        "conditions": [
            "송은이는 집에서 출발해 문방구를 들른 뒤 학교로 갑니다.",
            "집에서 문방구까지의 거리는 487 m입니다.",
            "문방구에서 학교까지의 거리는 295 m입니다.",
        ],
    },
    "given": [
        {
            "ref": "relation.distance_home_store",
            "value": {
                "distance": 487,
                "unit": "m",
                "from": "place.home",
                "to": "place.stationery_store",
            },
        },
        {
            "ref": "relation.distance_store_school",
            "value": {
                "distance": 295,
                "unit": "m",
                "from": "place.stationery_store",
                "to": "place.school",
            },
        },
    ],
    "target": {
        "ref": "answer.total_distance",
        "type": "distance",
    },
    "understanding": {
        "summary": (
            "집에서 학교까지 바로 간 거리가 아니라, 집에서 문방구까지 간 거리와 "
            "문방구에서 학교까지 간 거리를 모두 더해야 하는 문제입니다."
        ),
        "facts": [
            {
                "ref": "relation.distance_home_store",
                "label": "집에서 문방구까지의 거리",
                "value": 487,
                "unit": "m",
                "source": "explicit",
            },
            {
                "ref": "relation.distance_store_school",
                "label": "문방구에서 학교까지의 거리",
                "value": 295,
                "unit": "m",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "answer.total_distance",
                "label": "집에서 문방구를 거쳐 학교까지 간 전체 거리",
                "unit": "m",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "part_part_whole",
            "statement": "두 구간의 거리를 더하면 전체 이동 거리가 됩니다.",
            "symbolic": "487 m + 295 m = total_distance",
            "uses": [
                "relation.distance_home_store",
                "relation.distance_store_school",
            ],
            "result": "answer.total_distance",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "집에서 문방구까지의 거리",
                    "문방구에서 학교까지의 거리",
                    "집에서 문방구를 거쳐 학교까지 간 전체 거리",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.operation",
                "type": "multiple_choice",
                "prompt": "전체 이동 거리를 구하려면 어떤 계산을 해야 하나요?",
                "choices": [
                    "487과 295를 더합니다.",
                    "487에서 295를 뺍니다.",
                    "487과 295를 곱합니다.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 뜻을 자기 말로 설명해 볼까요?",
            "template": "{first_distance}와 {second_distance}를 더해 전체 거리를 구합니다.",
            "answer": "집에서 문방구까지 487 m와 문방구에서 학교까지 295 m를 더합니다.",
        },
    },
    "method": "두 이동 구간의 거리를 더해 전체 이동 거리를 구합니다.",
    "plan": [
        "집에서 문방구까지의 거리 487 m를 확인합니다.",
        "문방구에서 학교까지의 거리 295 m를 확인합니다.",
        "두 거리를 더합니다.",
        "계산 결과에 단위 m를 붙입니다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "goal": "두 구간의 거리를 더하는 식을 세웁니다.",
            "uses": [
                "relation.distance_home_store",
                "relation.distance_store_school",
            ],
            "expr": "487 + 295",
            "value": {
                "expression": "487 + 295",
            },
            "explanation": "집에서 학교까지 가는 동안 지나간 두 구간의 거리를 모두 더합니다.",
        },
        {
            "id": "step.2",
            "goal": "487 + 295를 계산합니다.",
            "uses": ["step.1"],
            "expr": "487 + 295 = 782",
            "value": {
                "distance": 782,
                "unit": "m",
                "ref": "answer.total_distance",
            },
            "explanation": (
                "일의 자리에서 7+5=12이므로 2를 쓰고 1을 받아올림합니다. "
                "십의 자리에서 8+9+1=18이므로 8을 쓰고 1을 받아올림합니다. "
                "백의 자리에서 4+2+1=7이므로 합은 782입니다."
            ),
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "description": "전체 거리 782 m에서 두 번째 구간 295 m를 빼면 첫 번째 구간 487 m가 됩니다.",
            "expr": "782 - 295",
            "expected": 487,
            "actual": 487,
            "pass": True,
        },
        {
            "id": "check.2",
            "description": "두 구간이 모두 양수이므로 전체 거리는 각 구간보다 커야 합니다.",
            "expr": "782 > 487 and 782 > 295",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [
            {
                "id": "slot.expression_blank",
                "type": "expression",
                "value": "487 + 295 = 782",
                "unit": "",
            },
            {
                "id": "slot.answer_blank",
                "type": "number",
                "value": 782,
                "unit": "m",
            },
        ],
        "choices": [],
        "answer_key": [
            {
                "blank_id": "slot.expression_blank",
                "value": "487 + 295 = 782",
                "unit": "",
            },
            {
                "blank_id": "slot.answer_blank",
                "value": 782,
                "unit": "m",
            },
        ],
        "value": 782,
        "unit": "m",
        "sentence": "집에서 문방구를 거쳐 학교까지의 거리는 782 m입니다.",
    },
}


SOLVABLE.update(
    {
        "inputs": {
            "target_label": "집에서 문구점을 거쳐 학교까지 간 전체 거리",
            "unit": "m",
            "quantities": {
                "home_to_store_distance": 487,
                "store_to_school_distance": 295,
            },
            "conditions": [
                "집에서 문구점까지의 거리는 487 m입니다.",
                "문구점에서 학교까지의 거리는 295 m입니다.",
                "문구점을 거쳐 학교까지 가므로 두 구간의 거리를 더합니다.",
            ],
        },
        "given": [
            {
                "ref": "relation.distance_home_store",
                "value": {
                    "distance": 487,
                    "unit": "m",
                    "from": "place.home",
                    "to": "place.stationery_store",
                },
            },
            {
                "ref": "relation.distance_store_school",
                "value": {
                    "distance": 295,
                    "unit": "m",
                    "from": "place.stationery_store",
                    "to": "place.school",
                },
            },
        ],
        "target": {
            "ref": "answer.total_distance",
            "type": "distance",
        },
        "understanding": {
            "summary": "집에서 문구점까지 간 거리와 문구점에서 학교까지 간 거리를 더해 전체 이동 거리를 구하는 문제입니다.",
            "facts": [
                {
                    "ref": "relation.distance_home_store",
                    "label": "집에서 문구점까지의 거리",
                    "value": 487,
                    "unit": "m",
                    "source": "explicit",
                },
                {
                    "ref": "relation.distance_store_school",
                    "label": "문구점에서 학교까지의 거리",
                    "value": 295,
                    "unit": "m",
                    "source": "explicit",
                },
            ],
            "unknowns": [
                {
                    "ref": "answer.total_distance",
                    "label": "집에서 문구점을 거쳐 학교까지 간 전체 거리",
                    "unit": "m",
                    "source": "unknown",
                }
            ],
            "relation": {
                "type": "part_part_whole",
                "statement": "전체 거리는 지나간 두 구간의 거리를 합한 값입니다.",
                "symbolic": "487 m + 295 m = total_distance",
                "uses": [
                    "relation.distance_home_store",
                    "relation.distance_store_school",
                ],
                "result": "answer.total_distance",
            },
            "diagnostic_questions": [
                {
                    "id": "understand.target",
                    "type": "multiple_choice",
                    "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                    "choices": [
                        "집에서 문구점까지의 거리",
                        "문구점에서 학교까지의 거리",
                        "집에서 문구점을 거쳐 학교까지 간 전체 거리",
                    ],
                    "answer_index": 2,
                },
                {
                    "id": "understand.operation",
                    "type": "multiple_choice",
                    "prompt": "전체 거리를 구하려면 어떤 계산을 해야 하나요?",
                    "choices": [
                        "487과 295를 더합니다.",
                        "487에서 295를 뺍니다.",
                        "487과 295를 곱합니다.",
                    ],
                    "answer_index": 0,
                },
            ],
            "student_restatement": {
                "prompt": "문제의 뜻을 말해 볼까요?",
                "template": "{first_distance}와 {second_distance}를 더해 전체 거리를 구합니다.",
                "answer": "집에서 문구점까지 487 m와 문구점에서 학교까지 295 m를 더해 전체 거리를 구합니다.",
            },
        },
        "method": "문구점을 거쳐 가는 길이므로 두 이동 구간의 거리를 더해 전체 거리를 구합니다.",
        "plan": [
            "집에서 문구점까지의 거리 487 m를 확인합니다.",
            "문구점에서 학교까지의 거리 295 m를 확인합니다.",
            "두 거리를 더하는 식을 세웁니다.",
            "487 + 295를 계산하고 단위 m를 붙입니다.",
        ],
        "steps": [
            {
                "id": "step.expression",
                "goal": "전체 거리를 구하는 식을 세웁니다.",
                "uses": [
                    "relation.distance_home_store",
                    "relation.distance_store_school",
                ],
                "expr": "487 + 295",
                "value": {
                    "expression": "487 + 295",
                },
                "explanation": "집에서 학교까지 가는 동안 문구점을 거치므로, 집에서 문구점까지의 거리와 문구점에서 학교까지의 거리를 모두 더합니다.",
            },
            {
                "id": "step.calculate",
                "goal": "487 + 295를 계산합니다.",
                "uses": ["step.expression"],
                "expr": "487 + 295",
                "value": 782,
                "explanation": "487 + 295 = 782이므로 전체 거리는 782 m입니다.",
            },
        ],
        "checks": [
            {
                "id": "check.subtract",
                "description": "전체 거리 782 m에서 두 번째 구간 295 m를 빼면 첫 번째 구간 487 m가 됩니다.",
                "expr": "782 - 295",
                "expected": 487,
                "actual": 487,
                "pass": True,
            },
            {
                "id": "check.size",
                "description": "두 구간이 모두 양수이므로 전체 거리는 각 구간보다 커야 합니다.",
                "expr": "782 > 487 and 782 > 295",
                "expected": True,
                "actual": True,
                "pass": True,
            },
        ],
        "answer": {
            "blanks": [
                {
                    "id": "slot.expression_blank",
                    "type": "expression",
                    "value": "487 + 295 = 782",
                    "unit": "",
                },
                {
                    "id": "slot.answer_blank",
                    "type": "number",
                    "value": 782,
                    "unit": "m",
                },
            ],
            "choices": [],
            "answer_key": [
                {
                    "blank_id": "slot.expression_blank",
                    "value": "487 + 295 = 782",
                    "unit": "",
                },
                {
                    "blank_id": "slot.answer_blank",
                    "value": 782,
                    "unit": "m",
                },
            ],
            "value": 782,
            "unit": "m",
            "sentence": "집에서 문구점을 거쳐 학교까지 간 거리는 782 m입니다.",
        },
    }
)


SEMANTIC_OVERRIDE["answer"] = SOLVABLE["answer"]
