from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_009008",
        title="선을 ㄱㄴ을 바르게 그린 것을 선택하세요.",
        canvas=Canvas(width=800.0, height=320.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_num", "slot.q_text"),
            ),
            Region(
                id="region.options",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.opt1.line",
                    "slot.opt1.pt1",
                    "slot.opt1.pt2",
                    "slot.opt1.lb1",
                    "slot.opt1.lb2",
                    "slot.opt2.line",
                    "slot.opt2.pt1",
                    "slot.opt2.pt2",
                    "slot.opt2.lb1",
                    "slot.opt2.lb2",
                    "slot.opt3.line",
                    "slot.opt3.pt1",
                    "slot.opt3.pt2",
                    "slot.opt3.lb1",
                    "slot.opt3.lb2",
                ),
            ),
            Region(
                id="region.answer",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.answer.line", "slot.answer.pt1", "slot.answer.pt2"),
            ),
            Region(id="region.explanation", role="note", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q_num",
                prompt="",
                text="47.",
                style_role="question",
                x=24.0,
                y=24.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q_text",
                prompt="",
                text="선을 ㄱㄴ을 바르게 그린 것을 선택하세요.",
                style_role="question",
                x=60.0,
                y=24.0,
                font_size=28,
            ),
            LineSlot(id="slot.opt1.line", prompt="", x1=110.0, y1=104.0, x2=280.0, y2=64.0),
            CircleSlot(id="slot.opt1.pt1", prompt="", cx=100.0, cy=107.0, r=3.5, fill="#222222"),
            CircleSlot(id="slot.opt1.pt2", prompt="", cx=286.0, cy=63.0, r=3.5, fill="#222222"),
            TextSlot(
                id="slot.opt1.lb1",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=92.0,
                y=92.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt1.lb2",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=284.0,
                y=46.0,
                font_size=28,
            ),
            LineSlot(id="slot.opt2.line", prompt="", x1=336.0, y1=106.0, x2=519.0, y2=63.0),
            CircleSlot(id="slot.opt2.pt1", prompt="", cx=326.0, cy=109.0, r=3.5, fill="#222222"),
            CircleSlot(id="slot.opt2.pt2", prompt="", cx=521.0, cy=63.0, r=3.5, fill="#222222"),
            TextSlot(
                id="slot.opt2.lb1",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=318.0,
                y=92.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt2.lb2",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=501.0,
                y=46.0,
                font_size=28,
            ),
            LineSlot(id="slot.opt3.line", prompt="", x1=555.0, y1=111.0, x2=740.0, y2=67.0),
            CircleSlot(id="slot.opt3.pt1", prompt="", cx=550.0, cy=110.0, r=3.5, fill="#222222"),
            CircleSlot(id="slot.opt3.pt2", prompt="", cx=744.0, cy=63.0, r=3.5, fill="#222222"),
            TextSlot(
                id="slot.opt3.lb1",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=540.0,
                y=92.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt3.lb2",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=726.0,
                y=46.0,
                font_size=28,
            ),
            LineSlot(id="slot.answer.line", prompt="", x1=55.0, y1=195.0, x2=228.0, y2=150.0),
            CircleSlot(id="slot.answer.pt1", prompt="", cx=52.0, cy=196.0, r=3.5, fill="#222222"),
            CircleSlot(id="slot.answer.pt2", prompt="", cx=229.0, cy=151.0, r=3.5, fill="#222222"),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_009008",
    "problem_type": "도형_선분_선택",
    "metadata": {
        "language": "ko",
        "question": "선을 ㄱㄴ을 바르게 그린 것을 선택하세요.",
        "instruction": "점 ㄱ과 점 ㄴ을 곧게 이은 선분을 고르는 문제이다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.point_g", "type": "point", "label": "ㄱ"},
            {"id": "obj.point_n", "type": "point", "label": "ㄴ"},
            {
                "id": "obj.segment_gn",
                "type": "segment",
                "endpoints": ["obj.point_g", "obj.point_n"],
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.point_g", "obj.point_n"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.connect_points"],
            },
            "plan": {
                "method": "identify_matching_diagram",
                "description": "ㄱ과 ㄴ을 곧게 이은 선분이 표시된 그림을 찾는다.",
            },
            "execute": {"expected_operations": ["compare_diagrams", "check_endpoints"]},
            "review": {"check_methods": ["endpoint_match_check", "straight_segment_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "correct_diagram_choice",
            "description": "ㄱ과 ㄴ을 곧게 이은 선분이 그려진 보기",
        },
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009008",
    "problem_type": "도형_선분_선택",
    "inputs": {
        "total_ticks": 0,
        "target_label": "ㄱㄴ을 바르게 그린 그림",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.point_g", "value": {"label": "ㄱ"}},
        {"ref": "obj.point_n", "value": {"label": "ㄴ"}},
    ],
    "target": {"ref": "answer.target", "type": "correct_diagram_choice"},
    "method": "identify_matching_diagram",
    "plan": ["점 ㄱ과 점 ㄴ이 주어진다.", "두 점을 곧게 이은 선분과 같은 그림을 찾는다."],
    "steps": [{"id": "step.1", "expr": "ㄱ과 ㄴ을 잇는 선분 찾기", "value": "diagram_match"}],
    "checks": [
        {
            "id": "check.1",
            "expr": "선분의 양끝이 ㄱ과 ㄴ인지 확인",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "correct_diagram_choice",
            "description": "ㄱ과 ㄴ을 곧게 이은 선분이 그려진 보기",
        },
        "value": 1,
        "unit": "",
    },
}
