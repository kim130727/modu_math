from __future__ import annotations

from modu_math.dsl import BlankSlot, Canvas, ProblemTemplate, Region, TextBoxSlot


PROBLEM_ID = "new_problem_20260916"
PROBLEM_TITLE = "new_problem_20260916"

ANSWER = {
    "blanks": [
        {
            "id": "slot.answer",
            "label": "정답",
            "expected": "",
            "unit": "",
        },
    ],
    "choices": [
        {
            "id": "choice.A",
            "label": "A",
            "text": "",
        },
        {
            "id": "choice.B",
            "label": "B",
            "text": "",
        },
        {
            "id": "choice.C",
            "label": "C",
            "text": "",
        },
        {
            "id": "choice.D",
            "label": "D",
            "text": "",
        },
    ],
    "answer_key": [
        {
            "blank_id": "slot.answer",
            "value": "",
            "unit": "",
        },
    ],
    "confidence": 1.0,
    "target": {
        "type": "draft_answer",
        "description": "정답",
    },
    "value": "",
    "unit": "",
}


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=900, height=420, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=("slot.question", "slot.instruction"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.work_area",),
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
                text="문제를 입력하세요.",
                prompt="학생에게 제시할 문제 문장",
                semantic_role="question",
                x=48,
                y=40,
                width=804,
                height=64,
                font_size=28,
                line_height=1.35,
            ),
            TextBoxSlot(
                id="slot.instruction",
                text="알맞은 답을 구하세요.",
                prompt="풀이 또는 응답 지시문",
                semantic_role="instruction",
                x=48,
                y=112,
                width=804,
                height=44,
                font_size=20,
                line_height=1.35,
            ),
            TextBoxSlot(
                id="slot.work_area",
                text="",
                prompt="그림, 표, 수식 등 문제 자료를 배치하는 영역",
                semantic_role="work_area",
                x=48,
                y=176,
                width=520,
                height=184,
                font_size=22,
                line_height=1.35,
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
        tags=("draft", "authoring-template", "schema-compliant"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "draft_math_problem",
    "metadata": {
        "title": PROBLEM_TITLE,
        "tags": ["draft", "authoring-template"],
        "language": "ko",
        "question": "문제를 입력하세요.",
        "instruction": "알맞은 답을 구하세요.",
        "required_layout_ids": [],
        "authoring_status": "draft",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.problem",
                "type": "math_problem",
                "properties": {
                    "source": "new_file_template",
                    "description": "새 문제 제작용 기본 객체입니다.",
                },
            },
            {
                "id": "obj.answer",
                "type": "answer",
                "properties": {
                    "label": "정답",
                    "value": "",
                    "unit": "",
                },
            },
        ],
        "relations": [],
    },
    "answer": ANSWER,
}

SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "draft_math_problem",
    "inputs": {
        "target_label": "정답",
        "unit": "",
        "quantities": {
            "answer": "",
        },
        "conditions": [
            "문제에 주어진 조건을 입력하세요.",
        ],
    },
    "given": [
        {
            "ref": "obj.problem",
            "value": "문제를 입력하세요.",
        },
        {
            "ref": "obj.answer",
            "value": "",
        },
    ],
    "target": {
        "ref": "answer.value",
        "type": "draft_answer",
    },
    "understanding": {
        "summary": "臾몄젣?먯꽌 二쇱뼱吏?寃껉낵 援ы빐???섎뒗 寃껋쓣 援щ텇?섎뒗 珥덇린 ?댄빐 ?④퀎",
        "facts": [
            {
                "ref": "obj.problem",
                "label": "臾몄젣?먯꽌 二쇱뼱吏?寃?",
                "value": "臾몄젣瑜??낅젰?섏꽭??",
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "answer.value",
                "label": "援ы빐???섎뒗 寃?",
                "unit": "",
            },
        ],
        "relation": {
            "type": "author_defined",
            "statement": "二쇱뼱吏??뺣낫瑜?蹂닿퀬 援ы빐???섎뒗 寃껋쓣 ?먮떒?⑸땲??",
            "uses": ["obj.problem"],
            "result": "answer.value",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "free_response",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
            },
        ],
    },
    "method": "author_defined_solution",
    "plan": [
        "문제에 주어진 값을 확인한다.",
        "조건에 맞는 풀이식을 세운다.",
        "계산 또는 추론으로 정답을 구한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "문제 조건 확인",
            "value": "",
            "explanation": "문제에 필요한 수량과 조건을 정리합니다.",
        },
        {
            "id": "step.2",
            "expr": "풀이식 작성",
            "value": "",
            "explanation": "정답을 구하는 식 또는 추론 과정을 작성합니다.",
        },
        {
            "id": "step.3",
            "expr": "정답 도출",
            "value": "",
            "explanation": "계산 결과 또는 선택한 보기를 정답으로 기록합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "정답 형식 확인",
            "expected": "",
            "actual": "",
            "pass": True,
        },
    ],
    "answer": ANSWER,
}
