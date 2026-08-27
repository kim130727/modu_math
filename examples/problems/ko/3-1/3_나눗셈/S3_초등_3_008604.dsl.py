from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    SpeakerSpec,
    TextSlot,
    speaker_group_slot_ids,
    speaker_group_slots,
)


def build_problem_template() -> ProblemTemplate:
    speakers = (
        SpeakerSpec(
            key="left",
            cx=220.0,
            bubble_cy=195.0,
            head_cy=340.0,
            text="몫은 13이야.",
            name="현태",
            hair="#4b1f16",
            shirt="#D7A0D7",
            bubble_width=150.0,
            bubble_height=82.0,
            tail_y=270.0,
            name_width=80.0,
            name_height=36.0,
            name_y=480.0,
            speech_font_size=24,
        ),
        SpeakerSpec(
            key="right",
            cx=565.0,
            bubble_cy=195.0,
            head_cy=340.0,
            text="나머지는 0으로\n나누어떨어져.",
            name="은수",
            hair="#1d1714",
            shirt="#8ED7E6",
            bubble_width=175.0,
            bubble_height=94.0,
            tail_y=270.0,
            name_width=80.0,
            name_height=36.0,
            name_y=480.0,
            speech_font_size=22,
            speech_text_dy=-3,
        ),
    )
    return ProblemTemplate(
        id="S3_초등_3_008604",
        title="문제를 바르게 설명한 사람의 이름을 선택하세요.",
        canvas=Canvas(width=785.0, height=559.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.expr_box",
                    "slot.expr_text",
                    *speaker_group_slot_ids(speakers),
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="문제를 바르게 설명한 사람의 이름을 선택하세요.",
                style_role="question",
                x=24,
                y=48,
                font_size=28,
                fill="#111111",
            ),
            RectSlot(
                id="slot.expr_box",
                prompt="",
                x=300,
                y=70,
                width=186,
                height=62,
                fill="none",
                stroke="#F4A340",
                stroke_width=2,
            ),
            TextSlot(
                id="slot.expr_text",
                prompt="",
                text="67 ÷ 5",
                style_role="choice",
                x=352,
                y=113,
                font_size=28,
                fill="#111111",
            ),
            *speaker_group_slots(speakers),
        ),
    )
