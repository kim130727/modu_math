from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, LineSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008975",
        title="반직선을 선택하세요",
        canvas=Canvas(width=760, height=240, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.no", "slot.q.text"),
            ),
            Region(
                id="region.options.top",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.opt1.line",
                    "slot.opt1.pt1",
                    "slot.opt1.pt2",
                    "slot.opt2.line1",
                    "slot.opt2.line2",
                    "slot.opt2.pt1",
                    "slot.opt2.pt2",
                    "slot.opt3.line",
                    "slot.opt3.pt1",
                    "slot.opt3.pt2",
                ),
            ),
            Region(
                id="region.answer",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.answer.line", "slot.answer.pt1", "slot.answer.pt2"),
            ),
            Region(id="region.explain", role="explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q.no",
                prompt="",
                text="□ 10.",
                style_role="question",
                x=12.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="반직선을 선택하세요.",
                style_role="question",
                x=92.0,
                y=26.0,
                font_size=28,
            ),
            LineSlot(id="slot.opt1.line", prompt="", x1=197.0, y1=82.0, x2=280.0, y2=45.0),
            CircleSlot(id="slot.opt1.pt1", prompt="", cx=197.0, cy=82.0, r=2.4, fill="#222222"),
            CircleSlot(id="slot.opt1.pt2", prompt="", cx=280.0, cy=45.0, r=2.4, fill="#222222"),
            LineSlot(id="slot.opt2.line1", prompt="", x1=386.0, y1=53.0, x2=403.0, y2=94.0),
            LineSlot(id="slot.opt2.line2", prompt="", x1=403.0, y1=94.0, x2=491.0, y2=80.0),
            CircleSlot(id="slot.opt2.pt1", prompt="", cx=386.0, cy=53.0, r=2.4, fill="#222222"),
            CircleSlot(id="slot.opt2.pt2", prompt="", cx=491.0, cy=80.0, r=2.4, fill="#222222"),
            LineSlot(id="slot.opt3.line", prompt="", x1=614.0, y1=53.0, x2=730.0, y2=95.0),
            CircleSlot(id="slot.opt3.pt1", prompt="", cx=614.0, cy=53.0, r=2.4, fill="#222222"),
            CircleSlot(id="slot.opt3.pt2", prompt="", cx=730.0, cy=95.0, r=2.4, fill="#222222"),
            LineSlot(id="slot.answer.line", prompt="", x1=82.0, y1=129.0, x2=180.0, y2=167.0),
            CircleSlot(id="slot.answer.pt1", prompt="", cx=82.0, cy=129.0, r=2.4, fill="#222222"),
            CircleSlot(id="slot.answer.pt2", prompt="", cx=180.0, cy=167.0, r=2.4, fill="#222222"),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008975",
    "problem_type": "도형_선의종류_선택",
    "metadata": {
        "language": "ko",
        "question": "반직선을 선택하세요.",
        "instruction": "보기 중 반직선을 고르는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.figure_1", "type": "line_figure"},
            {"id": "obj.figure_2", "type": "line_figure"},
            {"id": "obj.figure_3", "type": "line_figure"},
            {"id": "obj.figure_answer", "type": "line_figure", "marked": True},
            {
                "id": "obj.definition",
                "type": "definition_text",
                "text": "한 점에서 한쪽으로 끝없이 늘인 곧은 선",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.definition",
                    "obj.figure_1",
                    "obj.figure_2",
                    "obj.figure_3",
                    "obj.figure_answer",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.selects"],
            },
            "plan": {
                "method": "definition_matching",
                "description": "제시된 정의와 각 그림의 형태를 비교하여 반직선에 해당하는 것을 찾는다.",
            },
            "execute": {
                "expected_operations": ["compare_figures_by_definition", "identify_marked_choice"]
            },
            "review": {"check_methods": ["definition_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "figure_selection", "description": "반직선"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008975",
    "problem_type": "도형_선의종류_선택",
    "inputs": {
        "total_ticks": 0,
        "target_label": "반직선",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [{"ref": "obj.definition", "value": "한 점에서 한쪽으로 끝없이 늘인 곧은 선"}],
    "target": {"ref": "answer.target", "type": "figure_selection"},
    "method": "definition_matching",
    "plan": ["정의에 맞는 선의 종류를 찾는다.", "보기 중 해당하는 그림을 확인한다."],
    "steps": [
        {
            "id": "step.1",
            "expr": "definition = 한 점에서 한쪽으로 끝없이 늘인 곧은 선",
            "value": "반직선",
        }
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "definition_matches_target",
            "expected": "반직선",
            "actual": "반직선",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "figure_selection", "description": "반직선"},
        "value": 0,
        "unit": "",
    },
}
