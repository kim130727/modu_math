from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot, person_slots


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008608",
        title="몫이 다른 사람을 선택해 보세요.",
        canvas=Canvas(width=820, height=390, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)),
            Region(
                id="region.figures",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.name.left",
                    "slot.name.mid",
                    "slot.name.right",
                    "slot.figure.left.body",
                    "slot.figure.left.head",
                    "slot.figure.left.hair.cap",
                    "slot.figure.left.eye.left",
                    "slot.figure.left.eye.right",
                    "slot.figure.left.smile",
                    "slot.figure.mid.body",
                    "slot.figure.mid.head",
                    "slot.figure.mid.hair.cap",
                    "slot.figure.mid.eye.left",
                    "slot.figure.mid.eye.right",
                    "slot.figure.mid.smile",
                    "slot.figure.right.body",
                    "slot.figure.right.head",
                    "slot.figure.right.hair.cap",
                    "slot.figure.right.eye.left",
                    "slot.figure.right.eye.right",
                    "slot.figure.right.smile",
                ),
            ),
            Region(id="region.answer", role="explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(id="slot.q1", prompt="", text = '몫이 다른 사람을 선택해 보세요.', style_role="question", x = 125, y = 55, font_size = 30, max_width = 690),
            TextSlot(id="slot.box.left.text", prompt="", text = '30 ÷ 3', style_role="choice", x = 170, y = 140, font_size = 30),
            TextSlot(id="slot.box.mid.text", prompt="", text = '40 ÷ 2', style_role="choice", x = 385, y = 145, font_size = 30),
            TextSlot(id="slot.box.right.text", prompt="", text = '70 ÷ 7', style_role="choice", x = 610, y = 145, font_size = 30),
            *person_slots("slot.figure.left", cx=216.0, head_cy=188.0, hair="#4b1f16", shirt="#D7A0D7"),
            *person_slots("slot.figure.mid", cx=437.0, head_cy=188.0, hair="#1d1714", shirt="#8ED7E6"),
            *person_slots("slot.figure.right", cx=657.0, head_cy=188.0, hair="#5b3218", shirt="#F2C66D"),
            TextSlot(id="slot.name.left", prompt="", text = '은재', style_role="choice", x = 190, y = 305, font_size = 30),
            TextSlot(id="slot.name.mid", prompt="", text = '성환', style_role="choice", x = 415, y = 305, font_size = 30),
            TextSlot(id="slot.name.right", prompt="", text = '기영', style_role="choice", x = 635, y = 305, font_size = 30),
            
        ),
        diagrams=(), groups=(), constraints=(), tags=("초등", "수학", "나눗셈", "몫", "비교"),
    )

PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE={"problem_id":"S3_초등_3_008608","problem_type":"selection_by_division_result","metadata":{"language":"ko","question":"몫이 다른 사람을 선택해 보세요.","instruction":"세 사람의 나눗셈 결과를 비교해 몫이 다른 사람을 고르세요."},"domain":{"objects":[{"id":"obj.person.1","type":"person","name":"은재"},{"id":"obj.person.2","type":"person","name":"성환"},{"id":"obj.person.3","type":"person","name":"기영"},{"id":"obj.expr.1","type":"division_expression","text":"30 ÷ 3"},{"id":"obj.expr.2","type":"division_expression","text":"40 ÷ 2"},{"id":"obj.expr.3","type":"division_expression","text":"70 ÷ 7"}],"relations":[],"problem_solving":{"understand":{"given_refs":["obj.expr.1","obj.expr.2","obj.expr.3"],"target_ref":"answer.target","condition_refs":["rel.select_other"]},"plan":{"method":"compare_results","description":"각 나눗셈의 몫을 구해 다른 값을 가진 사람을 고른다."},"execute":{"expected_operations":["compute_division_results","compare_values","select_unique_person"]},"review":{"check_methods":["same_result_group_check","unique_result_check"]}}},"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"selected_person","description":"몫이 다른 사람"},"value":"성환","unit":""}}
SOLVABLE={"schema":"modu.solvable.v1.1","problem_id":"S3_초등_3_008608","problem_type":"selection_by_division_result","inputs":{"total_ticks":3,"target_label":"몫이 다른 사람","target_ticks":1,"target_count":1,"unit":""},"given":[{"ref":"obj.expr.1","value":{"text":"30 ÷ 3"}},{"ref":"obj.expr.2","value":{"text":"40 ÷ 2"}},{"ref":"obj.expr.3","value":{"text":"70 ÷ 7"}}],"target":{"ref":"answer.target","type":"selected_person"},"method":"compare_results","plan":["세 식의 몫을 구한다.","몫이 다른 값을 찾는다.","해당 사람을 선택한다."],"steps":[{"id":"step.1","expr":"30 ÷ 3","value":10},{"id":"step.2","expr":"40 ÷ 2","value":20},{"id":"step.3","expr":"70 ÷ 7","value":10},{"id":"step.4","expr":"다른 몫의 사람","value":"성환"}],"checks":[{"id":"check.1","expr":"10,20,10 비교","expected":"성환","actual":"성환","pass":True}],"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"selected_person","description":"몫이 다른 사람"},"value":"성환","unit":""}}
