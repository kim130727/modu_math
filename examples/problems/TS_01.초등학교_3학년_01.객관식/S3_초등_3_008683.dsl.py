from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
    SpeakerSpec,
    speaker_group_slot_ids,
    speaker_group_slots,
)


def build_problem_template() -> ProblemTemplate:
    speakers = (
        SpeakerSpec(
            key="girl",
            cx = ((790.0) + (-230.0)) + (45.0), head_cy = ((395.0) + (-5.0)) + (10.0), bubble_cy = ((354.0) + (-5.0)) + (10.0), text="큰 원의 반지름을\n( 지름, 반지름 )으로 하는\n작은 원을 2개 그려.",
            name="지혜",
            hair="#4B260B",
            shirt="#F16078",
            bow="#E85BA6",
            pigtails=True,
            bubble_width=285.0,
            bubble_height=118.0,
            tail_y = ((350.0) + (-5.0)) + (10.0), name_y = ((468.0) + (-5.0)) + (10.0), speech_font_size=21,
            speech_text_dy=-26,
        ),
    )
    character_slot_ids = tuple(
        slot_id for slot_id in speaker_group_slot_ids(speakers) if ".person." in slot_id
    )
    character_slots = tuple(
        slot for slot in speaker_group_slots(speakers) if ".person." in slot.id
    )

    return ProblemTemplate(
        id="S3_초등_3_008683",
        title="원을 그리는 방법",
        canvas=Canvas(width=940, height=900, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1",
                    "slot.q2",
                    "slot.box1",
                    "slot.box2",
                    "slot.box2_2",
                    "slot.diagram1.frame",
                    "slot.diagram1.circle",
                    "slot.diagram1.center",
                    "slot.diagram1.ray1",
                    "slot.diagram1.ray2",
                    "slot.diagram1.ray3",
                    "slot.diagram1.ray4",
                    "slot.diagram1.ray5",
                    "slot.diagram1.label1",
                    "slot.diagram1.label2",
                    "slot.diagram1.label3",
                    "slot.diagram1.label4",
                    "slot.diagram1.label5",
                    "slot.bubble1",
                    "slot.box3",
                    "slot.choice1",
                    "slot.choice2",
                    'slot.bubble1.copy3',
                    *character_slot_ids,
                ),
            ),
        ),
        slots=(TextSlot(
                id="slot.q1",
                prompt="",
                text = '    다음과 같은 방법으로 원을 그렸습니다. 그린 원을 보고 ', style_role="question",
                x = 75, y = 120, font_size = 30),
            TextSlot(
                id="slot.q2",
                prompt="",
                text = '알맞은 말을 선택하세요.', style_role="question",
                x = 75, y = 165, font_size = 30),
            RectSlot(
                id="slot.box1",
                prompt="",
                x = 80, y = 195, width = 760, height = 120, fill="#dcd7ef",
            ),
            TextSlot(
                id="slot.box2",
                prompt="",
                text = '① 빨간색 점에서 2 cm 떨어진 위치에 점을 찍습니다.', style_role="question",
                x = 115, y = 240, font_size = 30),
            TextSlot(
                id="slot.box2_2",
                prompt="",
                text = '② 찍은 점들을 이어 원을 그립니다.', style_role="question",
                x = 115, y = 286, font_size = 30),
            RectSlot(id="slot.diagram1.frame", prompt="", x = 605, y = 345, width = 235, height = 240),
            CircleSlot(id="slot.diagram1.circle", prompt="", cx = 725, cy = 465, r = 120, fill="none"),
            CircleSlot(id="slot.diagram1.center", prompt="", cx = 725, cy = 465, r = 5, fill="#ff4db8"),
            LineSlot(id="slot.diagram1.ray1", prompt="", x1 = 725, y1 = 465, x2 = 725, y2 = 345, stroke="#5dbbff", stroke_dasharray="6 6"),
            LineSlot(id="slot.diagram1.ray2", prompt="", x1 = 725, y1 = 465, x2 = 785, y2 = 360, stroke="#5dbbff", stroke_dasharray="6 6"),
            LineSlot(id="slot.diagram1.ray3", prompt="", x1 = 725, y1 = 465, x2 = 825, y2 = 405, stroke="#5dbbff", stroke_dasharray="6 6"),
            LineSlot(id="slot.diagram1.ray4", prompt="", x1 = 725, y1 = 465, x2 = 840, y2 = 465, stroke="#5dbbff", stroke_dasharray="6 6"),
            LineSlot(id="slot.diagram1.ray5", prompt="", x1 = 725, y1 = 465, x2 = 825, y2 = 525, stroke="#9aa0a6", stroke_dasharray="6 6"),
            TextSlot(id="slot.diagram1.label1", prompt="", text = '2 cm', style_role="question", x = 730, y = 380, font_size = 30),
            TextSlot(id="slot.diagram1.label2", prompt="", text = '2 cm', style_role="question", x = 685, y = 415, font_size = 30),
            TextSlot(id="slot.diagram1.label3", prompt="", text = '2 cm', style_role="question", x = 765, y = 420, font_size = 30),
            TextSlot(id="slot.diagram1.label4", prompt="", text = '2 cm', style_role="question", x = 780, y = 470, font_size = 30),
            TextSlot(id="slot.diagram1.label5", prompt="", text = '2 cm', style_role="question", x = 770, y = 500, font_size = 30),
            TextSlot(
                id="slot.bubble1",
                prompt="",
                text = '        줄로 연결한 막대를 돌려', style_role="question",
                x = 280, y = 375, font_size = 30),
            RectSlot(id="slot.box3", prompt="", x = 85, y = 672, width = 760, height = 115, fill="#ffffff"),
            TextSlot(
                id="slot.choice1",
                prompt="",
                text = '자를 이용하여 점을 더 ( 많이 , 적게 ) 찍은 다음, 점들을 이', style_role="question",
                x = 120, y = 717, font_size = 30),
            TextSlot(
                id="slot.choice2",
                prompt="",
                text = '으면 원을 좀 더 정확하게 그릴 수 있습니다.', style_role="question",
                x = 115, y = 762, font_size = 30),TextSlot(id = 'slot.bubble1.copy3', prompt = '', text = '그린 원과 비슷한 원이 그려지는구나.  ', x = 130, y = 420, font_size = 30, fill = '#111111'),
            *character_slots,
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008683",
    "problem_type": "sentence_choice",
    "metadata": {
        "language": "ko",
        "question": "원을 그리는 방법을 보고 알맞은 말을 선택하는 문제",
        "instruction": "그린 원을 보고 알맞은 말을 선택하세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.circle_drawing",
                "type": "drawing_process",
                "description": "점을 찍고 이어 원을 그리는 방법",
            },
            {
                "id": "obj.points",
                "type": "point_set",
                "description": "원 둘레에 찍는 점들",
            },
            {
                "id": "obj.center",
                "type": "point",
                "description": "빨간색 점에서 떨어진 기준점",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle_drawing", "rel.distance"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.more_points_more_accuracy"],
            },
            "plan": {
                "method": "visual_comparison",
                "description": "그림의 점 찍기 밀도를 비교하여 알맞은 말을 고른다.",
            },
            "execute": {
                "expected_operations": ["compare_point_density", "choose_correct_word"]
            },
            "review": {"check_methods": ["match_with_visible_answer_mark"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_word", "description": "빈칸에 들어갈 알맞은 말"},
        "value": "많이",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008683",
    "problem_type": "sentence_choice",
    "inputs": {
        "total_ticks": 1,
        "target_label": "빈칸",
        "target_ticks": 1,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle_drawing", "value": "점을 찍고 이어 원을 그리는 방법"},
        {"ref": "rel.distance", "value": "같은 거리"},
    ],
    "target": {"ref": "answer.target", "type": "choice_word"},
    "method": "visual_comparison",
    "plan": [
        "그림에서 점을 찍는 개수와 밀도를 비교한다.",
        "더 정확한 원을 그리는 데 필요한 말을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "그림 비교: 점을 더 많이 찍은 경우가 더 정확함",
            "value": "많이",
        }
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "빈칸 선택이 그림의 의미와 맞는가",
            "expected": "많이",
            "actual": "많이",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_word", "description": "빈칸에 들어갈 알맞은 말"},
        "value": "많이",
        "unit": "",
    },
}
