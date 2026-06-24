from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, LineSlot, PathSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008981",
        title="같을 선택하세요.",
        canvas=Canvas(width=720, height=240, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.num", "slot.title")
            ),
            Region(
                id="region.shapes",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.shape.1a",
                    "slot.shape.1b",
                    "slot.shape.1c",
                    "slot.shape.2a",
                    "slot.shape.2b",
                    "slot.shape.3a",
                    "slot.shape.3b",
                    "slot.shape.3c",
                    "slot.shape.4a",
                    "slot.shape.4b",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.num",
                prompt="",
                text="16.",
                style_role="question",
                x=16.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.title",
                prompt="",
                text="같을 선택하세요.",
                style_role="question",
                x=60.0,
                y=28.0,
                font_size=28,
            ),
            LineSlot(id="slot.shape.1a", prompt="", x1=154.0, y1=56.0, x2=186.0, y2=88.0),
            LineSlot(id="slot.shape.1b", prompt="", x1=186.0, y1=88.0, x2=214.0, y2=56.0),
            PathSlot(id="slot.shape.1c", prompt="", d="M 154 56 Q 170 50 186 88 Q 202 50 214 56"),
            LineSlot(id="slot.shape.2a", prompt="", x1=382.0, y1=48.0, x2=454.0, y2=72.0),
            LineSlot(id="slot.shape.2b", prompt="", x1=382.0, y1=96.0, x2=454.0, y2=72.0),
            PathSlot(id="slot.shape.3a", prompt="", d="M 576 44 Q 594 80 630 96"),
            LineSlot(id="slot.shape.3b", prompt="", x1=576.0, y1=44.0, x2=676.0, y2=44.0),
            PathSlot(id="slot.shape.3c", prompt="", d="M 630 96 Q 662 96 676 96"),
            LineSlot(id="slot.shape.4a", prompt="", x1=46.0, y1=124.0, x2=132.0, y2=146.0),
            LineSlot(id="slot.shape.4b", prompt="", x1=46.0, y1=160.0, x2=132.0, y2=146.0),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008981",
    "problem_type": "도형_식별",
    "metadata": {
        "language": "ko",
        "question": "같을 선택하세요.",
        "instruction": "도형을 보고 같은 것을 찾는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.shape_candidate_1", "type": "shape"},
            {"id": "obj.shape_candidate_2", "type": "shape"},
            {"id": "obj.shape_candidate_3", "type": "shape"},
            {"id": "obj.shape_answer", "type": "shape"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.shape_candidate_1",
                    "obj.shape_candidate_2",
                    "obj.shape_candidate_3",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.mentioned_in_explanation"],
            },
            "plan": {
                "method": "shape_matching",
                "description": "설명 문장과 같은 성질을 가진 도형을 고른다.",
            },
            "execute": {
                "expected_operations": ["compare_shape_features", "match_with_description"]
            },
            "review": {"check_methods": ["description_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "shape", "description": "한 점에서 그은 두 반직선으로 이루어진 도형"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008981",
    "problem_type": "도형_식별",
    "inputs": {
        "total_ticks": 0,
        "target_label": "한 점에서 그은 두 반직선으로 이루어진 도형",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.shape_candidate_1", "value": {"type": "shape"}},
        {"ref": "obj.shape_candidate_2", "value": {"type": "shape"}},
        {"ref": "obj.shape_candidate_3", "value": {"type": "shape"}},
    ],
    "target": {"ref": "answer.target", "type": "shape"},
    "method": "shape_matching",
    "plan": ["설명 문장과 같은 도형의 성질을 찾는다.", "보기 도형들과 설명을 비교한다."],
    "steps": [
        {
            "id": "step.1",
            "expr": "설명 문장 확인",
            "value": "한 점에서 그은 두 반직선으로 이루어진 도형",
        },
        {"id": "step.2", "expr": "보기 도형 비교", "value": "TODO"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "설명 문장과 도형 성질이 일치하는지 확인",
            "expected": True,
            "actual": False,
            "pass": False,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "shape", "description": "한 점에서 그은 두 반직선으로 이루어진 도형"},
        "value": 0,
        "unit": "",
    },
}
