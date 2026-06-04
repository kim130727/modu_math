from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008598",
        title="나머지가 더 큰 것을 선택해 보세요.",
        canvas=Canvas(width=728, height=270, coordinate_mode="logical"),
        regions=(
            Region(id="region.header", role="stem", flow="absolute", slot_ids=("slot.qnum", "slot.title")),
            Region(id="region.choice", role="choices", flow="absolute", slot_ids=("slot.box.left", "slot.text.left", "slot.box.right", "slot.text.right")),
            Region(id="region.explanation", role="explanation", flow="absolute", slot_ids=("slot.compare",)),
        ),
        slots=(
            TextSlot(id="slot.qnum", prompt="", text="67.", style_role="question", x=28.0, y=26.0, font_size=28),
            TextSlot(id="slot.title", prompt="", text="나머지가 더 큰 것을 선택해 보세요.", style_role="question", x=70.0, y=26.0, font_size=28),
            RectSlot(id="slot.box.left", prompt="", x=249.0, y=46.0, width=184.0, height=76.0),
            TextSlot(id="slot.text.left", prompt="", text="504 ÷ 5", style_role="choice", x=295.0, y=95.0, font_size=28),
            RectSlot(id="slot.box.right", prompt="", x=504.0, y=46.0, width=184.0, height=76.0),
            TextSlot(id="slot.text.right", prompt="", text="467 ÷ 3", style_role="choice", x=550.0, y=95.0, font_size=28),
            TextSlot(id="slot.compare", prompt="", text="나머지의 크기를 비교하면 4 > 2 입니다.", style_role="body", x=66.0, y=236.0, font_size=28),
        ),
        diagrams=(), groups=(), constraints=(), tags=("초등", "수학", "나눗셈", "나머지", "비교"),
    )

PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
 "problem_id":"S3_초등_3_008598","problem_type":"division_remainder_comparison",
 "metadata":{"language":"ko","question":"나머지가 더 큰 것을 선택해 보세요.","instruction":"두 나눗셈의 나머지를 비교해 더 큰 쪽을 고르세요."},
 "domain":{"objects":[{"id":"obj.left_division","type":"division_expression","expression":"504 ÷ 5"},{"id":"obj.right_division","type":"division_expression","expression":"467 ÷ 3"},{"id":"obj.left_remainder","type":"remainder","value":4},{"id":"obj.right_remainder","type":"remainder","value":2}],"relations":[],"problem_solving":{"understand":{"given_refs":["obj.left_division","obj.right_division"],"target_ref":"answer.target","condition_refs":["rel.compare_remainders"]},"plan":{"method":"compare_remainders","description":"각 나눗셈의 나머지를 구해 더 큰 나머지를 고른다."},"execute":{"expected_operations":["identify_remainders","compare_values","select_larger_remainder_expression"]},"review":{"check_methods":["compare_two_remainders"]}}},
 "answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"selected_expression","description":"나머지가 더 큰 나눗셈식"},"value":"504 ÷ 5","unit":""}
}
SOLVABLE={
 "schema":"modu.solvable.v1.1","problem_id":"S3_초등_3_008598","problem_type":"division_remainder_comparison",
 "inputs":{"total_ticks":0,"target_label":"나머지가 더 큰 나눗셈식","target_ticks":0,"target_count":1,"unit":""},
 "given":[{"ref":"obj.left_division","value":{"expression":"504 ÷ 5"}},{"ref":"obj.right_division","value":{"expression":"467 ÷ 3"}}],
 "target":{"ref":"answer.target","type":"selected_expression"},"method":"compare_remainders",
 "plan":["두 나눗셈의 나머지를 구한다.","나머지 4와 2를 비교해 큰 쪽을 고른다."],
 "steps":[{"id":"step.1","expr":"504 ÷ 5","value":{"quotient":100,"remainder":4}},{"id":"step.2","expr":"467 ÷ 3","value":{"quotient":155,"remainder":2}},{"id":"step.3","expr":"비교","value":"4 > 2"}],
 "checks":[{"id":"check.1","expr":"4 > 2","expected":True,"actual":True,"pass":True}],
 "answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"selected_expression","description":"나머지가 더 큰 나눗셈식"},"value":"504 ÷ 5","unit":""}
}
