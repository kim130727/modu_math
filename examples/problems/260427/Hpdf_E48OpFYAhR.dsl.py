from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, LineSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_E48OpFYAhR",
        title="세 자리 수 뺄셈 복면산",
        canvas=Canvas(width=650, height=400, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.q2",
                    "slot.q3",
                    "slot.box",
                    "slot.num1.1",
                    "slot.num1.2",
                    "slot.num1.3",
                    "slot.num2.1",
                    "slot.num2.2",
                    "slot.num2.3",
                    "slot.minus",
                    "slot.line",
                    "slot.res.1",
                    "slot.res.2",
                    "slot.res.3",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="뺄셈식에서 같은 문자는 같은 숫자를 나타냅",
                style_role="question",
                x=12.0,
                y=40.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="니다. 각 자리의 숫자가 모두 다른 세 자리 수",
                style_role="question",
                x=12.0,
                y=80.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="㉠㉡㉢이 될 수 있는 수 중에서 가장 큰 수를 구하시오.",
                style_role="question",
                x=12.0,
                y=120.0,
                font_size=28,
            ),
            # Subtraction Box
            RectSlot(
                id="slot.box",
                prompt="",
                x=160,
                y=170,
                width=240,
                height=160,
                stroke="#333333",
                stroke_width=1.5,
                rx=10,
                ry=10,
                fill="none",
            ),
            # First Number: ㄱ ㄴ ㄷ
            TextSlot(id="slot.num1.1", prompt="", text="㉠", style_role="label", x=245, y=210, font_size=32),
            TextSlot(id="slot.num1.2", prompt="", text="㉡", style_role="label", x=285, y=210, font_size=32),
            TextSlot(id="slot.num1.3", prompt="", text="㉢", style_role="label", x=325, y=210, font_size=32),
            # Minus sign
            TextSlot(id="slot.minus", prompt="", text="－", style_role="label", x=195, y=250, font_size=32),
            # Second Number: ㄷ ㄴ ㄱ
            TextSlot(id="slot.num2.1", prompt="", text="㉢", style_role="label", x=245, y=250, font_size=32),
            TextSlot(id="slot.num2.2", prompt="", text="㉡", style_role="label", x=285, y=250, font_size=32),
            TextSlot(id="slot.num2.3", prompt="", text="㉠", style_role="label", x=325, y=250, font_size=32),
            # Line
            LineSlot(id="slot.line", prompt="", x1=190, y1=270, x2=370, y2=270, stroke="#333333", stroke_width=2),
            # Result: 3 9 6
            TextSlot(id="slot.res.1", prompt="", text="3", style_role="label", x=250, y=305, font_size=32),
            TextSlot(id="slot.res.2", prompt="", text="9", style_role="label", x=290, y=305, font_size=32),
            TextSlot(id="slot.res.3", prompt="", text="6", style_role="label", x=330, y=305, font_size=32),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("subtraction", "cryptarithmetic"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_E48OpFYAhR",
    "problem_type": "cryptarithmetic_subtraction",
    "metadata": {
        "language": "ko",
        "question": "㉠㉡㉢ - ㉢㉡㉠ = 396일 때, 각 자리 숫자가 모두 다른 세 자리 수 ㉠㉡㉢ 중 가장 큰 수 구하기",
        "instruction": "뺄셈식을 만족하는 ㉠, ㉡, ㉢을 찾고, 조건에 맞는 가장 큰 세 자리 수를 구한다.",
    },
    "domain": {
        "objects": [
            {"id": "var.ㄱ", "type": "digit_variable", "label": "㉠", "domain": [1, 9]},
            {"id": "var.ㄴ", "type": "digit_variable", "label": "㉡", "domain": [0, 9]},
            {"id": "var.ㄷ", "type": "digit_variable", "label": "㉢", "domain": [1, 9]},
            {
                "id": "expr.num_abc",
                "type": "polynomial_expression",
                "formula": "100 * var.ㄱ + 10 * var.ㄴ + var.ㄷ",
            },
            {
                "id": "expr.num_cba",
                "type": "polynomial_expression",
                "formula": "100 * var.ㄷ + 10 * var.ㄴ + var.ㄱ",
            },
        ],
        "relations": [
            {
                "id": "rel.subtraction_eq",
                "type": "equation",
                "left": "expr.num_abc - expr.num_cba",
                "right": 396,
            },
            {
                "id": "rel.unique_digits",
                "type": "all_different",
                "targets": ["var.ㄱ", "var.ㄴ", "var.ㄷ"],
            },
            {
                "id": "rel.maximize_target",
                "type": "optimization",
                "goal": "maximize",
                "target": "expr.num_abc",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["rel.subtraction_eq", "rel.unique_digits"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.maximize_target"],
            },
            "plan": {
                "method": "algebraic_deduction",
                "description": "(100ㄱ+10ㄴ+ㄷ) - (100ㄷ+10ㄴ+ㄱ) = 99(ㄱ-ㄷ) = 396 식을 통해 ㄱ-ㄷ=4임을 이용해 ㄱ이 최대인 경우를 찾고 ㄴ을 최대로 결정한다.",
            },
            "execute": {
                "expected_operations": [
                    "simplify_cryptarithmetic_equation",
                    "find_max_leading_digit",
                    "maximize_remaining_digit",
                ]
            },
            "review": {
                "check_methods": ["arithmetic_consistency", "digit_uniqueness_check"]
            },
        },
    },
    "answer": {
        "target": {
            "type": "three_digit_number",
            "ref": "expr.num_abc",
            "description": "조건을 만족하는 가장 큰 세 자리 수 ㉠㉡㉢",
        },
        "value": 985,
        "unit": "",
    },
}

SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_E48OpFYAhR',
    'problem_type': 'cryptarithmetic_subtraction',
    'inputs': {   'total_ticks': 396,
                  'target_label': '가장 큰 세 자리 수 ㉠㉡㉢',
                  'target_ticks': 985,
                  'target_count': 985,
                  'unit': ''},
    'plan': [   '100*ㄱ + 10*ㄴ + ㄷ - (100*ㄷ + 10*ㄴ + ㄱ) = 99*(ㄱ - ㄷ) = 396 식을 세운다.',
                'ㄱ - ㄷ = 4 이므로, ㄱ이 가장 큰 9일 때 ㄷ은 5가 된다.',
                'ㄱ=9, ㄷ=5이면서 세 숫자가 모두 달라야 하므로 ㄴ은 9, 5를 제외한 가장 큰 수 8이 된다.',
                '따라서 가장 큰 수는 985이다.'],
    'steps': [   {'id': 'step.s1', 'expr': '99 * (ㄱ - ㄷ) = 396', 'value': 396},
                 {'id': 'step.s2', 'expr': 'ㄱ - ㄷ = 396 / 99', 'value': 4},
                 {'id': 'step.s3', 'expr': 'ㄱ=9 일 때 ㄷ=9-4', 'value': 5},
                 {'id': 'step.s4', 'expr': 'ㄴ < 9, ㄴ ≠ 5 중 최대값', 'value': 8},
                 {'id': 'step.s5', 'expr': '100*9 + 10*8 + 5', 'value': 985}],
    'checks': [   {   'id': 'check.c1',
                      'expr': '985 - 589',
                      'expected': 396,
                      'actual': 396,
                      'pass': True},
                  {   'id': 'check.c2',
                      'expr': '9 != 8 != 5',
                      'expected': True,
                      'actual': True,
                      'pass': True}],
    'answer': {'value': 985, 'unit': '', 'derived_from': 'step.s5'}}
