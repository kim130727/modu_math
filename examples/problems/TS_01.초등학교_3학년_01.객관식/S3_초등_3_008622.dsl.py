from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008622",
        title="나눗셈의 나머지가 될 수 있는 수를 모두 선택해 보세요.",
        canvas=Canvas(width=952, height=272, coordinate_mode="logical"),
        regions=(Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.no", "slot.prompt", "slot.box", "slot.box.text", "slot.candidates")),),
        slots=(
            TextSlot(id="slot.no", prompt="", text="92.", style_role="question", x=18.0, y=24.0, font_size=28),
            TextSlot(id="slot.prompt", prompt="", text="나눗셈의 나머지가 될 수 있는 수를 모두 선택해 보세요.", style_role="question", x=70.0, y=24.0, font_size=28),
            RectSlot(id="slot.box", prompt="", x=383.0, y=43.0, width=196.0, height=76.0),
            TextSlot(id="slot.box.text", prompt="", text="□ ÷ 5", style_role="choice", x=440.0, y=92.0, font_size=28),
            TextSlot(id="slot.candidates", prompt="", text="( 1 , 2 , 3 , 4 , 5 , 6 )", style_role="question", x=377.0, y=148.0, font_size=28),
        ),
        diagrams=(), groups=(), constraints=(), tags=("초등", "수학", "나눗셈", "나머지", "선택형"),
    )

PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE={"problem_id":"S3_초등_3_008622","problem_type":"multiple_choice_remainder","metadata":{"language":"ko","question":"나눗셈의 나머지가 될 수 있는 수를 모두 선택해 보세요.","instruction":"주어진 수 중에서 나머지가 될 수 있는 수를 고르세요."},"domain":{"objects":[{"id":"obj.divisor","type":"number","value":5},{"id":"obj.candidates","type":"number_set","values":[1,2,3,4,5,6]}],"relations":[],"problem_solving":{"understand":{"given_refs":["obj.divisor","obj.candidates"],"target_ref":"answer.target","condition_refs":["rel.remainder_range"]},"plan":{"method":"compare_to_divisor","description":"나머지는 나누는 수보다 작다는 성질을 이용한다."},"execute":{"expected_operations":["compare_candidate_values","select_values_less_than_divisor"]},"review":{"check_methods":["less_than_divisor_check"]}}},"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"selected_numbers","description":"나머지가 될 수 있는 수"},"value":4,"unit":""}}
SOLVABLE={"schema":"modu.solvable.v1.1","problem_id":"S3_초등_3_008622","problem_type":"multiple_choice_remainder","inputs":{"total_ticks":6,"target_label":"나머지가 될 수 있는 수","target_ticks":4,"target_count":4,"unit":""},"given":[{"ref":"obj.divisor","value":5},{"ref":"obj.candidates","value":[1,2,3,4,5,6]}],"target":{"ref":"answer.target","type":"selected_numbers"},"method":"compare_to_divisor","plan":["나머지는 나누는 수보다 작다.","후보를 5와 비교해 5보다 작은 수를 고른다."],"steps":[{"id":"step.1","expr":"1<5,2<5,3<5,4<5,5<5,6<5","value":[True,True,True,True,False,False]},{"id":"step.2","expr":"선택한 수","value":[1,2,3,4]}],"checks":[{"id":"check.1","expr":"selected < 5","expected":True,"actual":True,"pass":True}],"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"selected_numbers","description":"나머지가 될 수 있는 수"},"value":4,"unit":""}}
