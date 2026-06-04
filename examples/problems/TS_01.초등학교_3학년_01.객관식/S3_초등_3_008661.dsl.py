from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    RectSlot,
    TextSlot,
    CircleSlot,
    LineSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008661",
        title="길이가 가장 긴 선분은 어느 것인가요?",
        canvas=Canvas(width=673.0, height=401.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_num", "slot.q_text"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle.outer",
                    "slot.circle.center",
                    "slot.line.top",
                    "slot.line.middle1",
                    "slot.line.middle2",
                    "slot.line.bottom",
                    "slot.lb.giyeok",
                    "slot.lb.nieun",
                    "slot.lb.digeut",
                    "slot.lb.rieul",
                    "slot.lb.mieum",
                    "slot.lb.bieup",
                    "slot.lb.sieut1",
                    "slot.lb.sieut2",
                    "slot.dot.center",
                ),
            ),
            Region(
                id="region.options",
                role="choices",
                flow="absolute",
                slot_ids=("slot.opt1", "slot.opt2", "slot.opt3", "slot.opt4"),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            RectSlot(
                id="slot.q_box", prompt="", x=10.0, y=16.0, width=13.0, height=13.0
            ),
            TextSlot(
                id="slot.q_num",
                prompt="",
                text="36.",
                style_role="question",
                x=35.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q_text",
                prompt="",
                text="길이가 가장 긴 선분은 어느 것인가요?",
                style_role="question",
                x=83.0,
                y=28.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle.outer",
                prompt="",
                cx=490.0,
                cy=124.0,
                r=76.0,
                fill="none",
            ),
            CircleSlot(
                id="slot.circle.center",
                prompt="",
                cx=490.0,
                cy=124.0,
                r=4.0,
                fill="none",
            ),
            LineSlot(
                id="slot.line.top", prompt="", x1=438.0, y1=84.0, x2=542.0, y2=84.0
            ),
            LineSlot(
                id="slot.line.middle1",
                prompt="",
                x1=426.0,
                y1=120.0,
                x2=554.0,
                y2=120.0,
            ),
            LineSlot(
                id="slot.line.middle2",
                prompt="",
                x1=430.0,
                y1=149.0,
                x2=550.0,
                y2=149.0,
            ),
            LineSlot(
                id="slot.line.bottom", prompt="", x1=438.0, y1=188.0, x2=542.0, y2=188.0
            ),
            TextSlot(
                id="slot.lb.giyeok",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=421.0,
                y=88.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.lb.nieun",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=546.0,
                y=88.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.lb.digeut",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=404.0,
                y=124.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.lb.rieul",
                prompt="",
                text="ㄹ",
                style_role="label",
                x=559.0,
                y=124.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.lb.mieum",
                prompt="",
                text="ㅁ",
                style_role="label",
                x=404.0,
                y=154.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.lb.bieup",
                prompt="",
                text="ㅂ",
                style_role="label",
                x=559.0,
                y=154.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.lb.sieut1",
                prompt="",
                text="스",
                style_role="label",
                x=408.0,
                y=196.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.lb.sieut2",
                prompt="",
                text="ㅅ",
                style_role="label",
                x=556.0,
                y=196.0,
                font_size=24,
            ),
            CircleSlot(
                id="slot.dot.center",
                prompt="",
                cx=490.0,
                cy=126.0,
                r=3.2,
                fill="#ff1493",
            ),
            TextSlot(
                id="slot.opt1",
                prompt="",
                text="① 선분 ㄱㄴ",
                style_role="choice",
                x=26.0,
                y=238.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt2",
                prompt="",
                text="② 선분 ㄷㄹ",
                style_role="choice",
                x=482.0,
                y=238.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt3",
                prompt="",
                text="③ 선분 ㅁㅂ",
                style_role="choice",
                x=26.0,
                y=283.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt4",
                prompt="",
                text="④ 선분 스ㅅ",
                style_role="choice",
                x=482.0,
                y=283.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008661",
    "problem_type": "geometry_segment_comparison",
    "metadata": {
        "language": "ko",
        "question": "길이가 가장 긴 선분은 어느 것인가요?",
        "instruction": "도형을 보고 보기 중 맞는 선분을 고르기",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.segment.gn", "type": "segment", "label": "ㄱㄴ"},
            {"id": "obj.segment.dr", "type": "segment", "label": "ㄷㄹ"},
            {"id": "obj.segment.mb", "type": "segment", "label": "ㅁㅂ"},
            {"id": "obj.segment.ss", "type": "segment", "label": "스ㅅ"},
            {"id": "obj.center_mark", "type": "mark", "description": "작은 원/점 표시"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.segment.gn",
                    "obj.segment.dr",
                    "obj.segment.mb",
                    "obj.segment.ss",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.dr_passes_center", "rel.max_length"],
            },
            "plan": {
                "method": "visual_comparison",
                "description": "원 안의 선분들 중 중심을 지나는 선분을 찾고, 보기에서 해당 선분을 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_center_passing_segment",
                    "match_with_choice",
                ]
            },
            "review": {"check_methods": ["compare_with_printed_explanation"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_selection", "description": "길이가 가장 긴 선분"},
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008661",
    "problem_type": "geometry_segment_comparison",
    "inputs": {
        "total_ticks": 0,
        "target_label": "가장 긴 선분",
        "target_ticks": 0,
        "target_count": 4,
        "unit": "",
    },
    "given": [
        {"ref": "obj.segment.gn", "value": {"label": "ㄱㄴ"}},
        {"ref": "obj.segment.dr", "value": {"label": "ㄷㄹ"}},
        {"ref": "obj.segment.mb", "value": {"label": "ㅁㅂ"}},
        {"ref": "obj.segment.ss", "value": {"label": "스ㅅ"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_selection"},
    "method": "visual_comparison",
    "plan": [
        "원 안의 네 선분을 비교한다.",
        "중심을 지나는 선분을 찾는다.",
        "보기에서 그 선분에 해당하는 번호를 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "중심을 지나는 선분 확인", "value": "ㄷㄹ"},
        {"id": "step.2", "expr": "보기와 대응", "value": 2},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "해설 문장과 선택지 일치 여부",
            "expected": 2,
            "actual": 2,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_selection", "description": "길이가 가장 긴 선분"},
        "value": 2,
        "unit": "",
    },
}
