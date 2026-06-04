from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


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
                    "slot.box.left",
                    "slot.box.mid",
                    "slot.box.right",
                    "slot.name.left",
                    "slot.name.mid",
                    "slot.name.right",
                    "slot.figure.left.head",
                    "slot.figure.left.body",
                    "slot.figure.left.eye1",
                    "slot.figure.left.eye2",
                    "slot.figure.left.mouth",
                    "slot.figure.mid.head",
                    "slot.figure.mid.body",
                    "slot.figure.mid.eye1",
                    "slot.figure.mid.eye2",
                    "slot.figure.mid.mouth",
                    "slot.figure.right.head",
                    "slot.figure.right.body",
                    "slot.figure.right.eye1",
                    "slot.figure.right.eye2",
                    "slot.figure.right.mouth",
                ),
            ),
            Region(id="region.answer", role="explanation", flow="absolute", slot_ids=("slot.a4",)),
        ),
        slots=(
            TextSlot(id="slot.q1", prompt="", text="78. 몫이 다른 사람을 선택해 보세요.", style_role="question", x=8.0, y=24.0, font_size=28),
            RectSlot(id="slot.box.left", prompt="", x=157.0, y=104.0, width=118.0, height=59.0),
            TextSlot(id="slot.box.left.text", prompt="", text="30 ÷ 3", style_role="choice", x=186.0, y=141.0, font_size=28),
            RectSlot(id="slot.box.mid", prompt="", x=377.0, y=104.0, width=118.0, height=59.0),
            TextSlot(id="slot.box.mid.text", prompt="", text="40 ÷ 2", style_role="choice", x=406.0, y=141.0, font_size=28),
            RectSlot(id="slot.box.right", prompt="", x=598.0, y=104.0, width=118.0, height=59.0),
            TextSlot(id="slot.box.right.text", prompt="", text="70 ÷ 7", style_role="choice", x=627.0, y=141.0, font_size=28),
            CircleSlot(id="slot.figure.left.head", prompt="", cx=216.0, cy=188.0, r=22.0, fill="#F3C0AD"),
            RectSlot(id="slot.figure.left.body", prompt="", x=205.0, y=204.0, width=22.0, height=30.0, rx=8.0, ry=8.0, fill="#D7A0D7", stroke="#D7A0D7"),
            CircleSlot(id="slot.figure.left.eye1", prompt="", cx=210.0, cy=184.0, r=2.5, fill="#222222"),
            CircleSlot(id="slot.figure.left.eye2", prompt="", cx=222.0, cy=184.0, r=2.5, fill="#222222"),
            LineSlot(id="slot.figure.left.mouth", prompt="", x1=210.0, y1=193.0, x2=222.0, y2=193.0, stroke="#C36A6A", stroke_dasharray=""),
            CircleSlot(id="slot.figure.mid.head", prompt="", cx=437.0, cy=188.0, r=22.0, fill="#F3C0AD"),
            RectSlot(id="slot.figure.mid.body", prompt="", x=426.0, y=204.0, width=22.0, height=30.0, rx=8.0, ry=8.0, fill="#8ED7E6", stroke="#8ED7E6"),
            CircleSlot(id="slot.figure.mid.eye1", prompt="", cx=431.0, cy=184.0, r=2.5, fill="#222222"),
            CircleSlot(id="slot.figure.mid.eye2", prompt="", cx=443.0, cy=184.0, r=2.5, fill="#222222"),
            LineSlot(id="slot.figure.mid.mouth", prompt="", x1=431.0, y1=193.0, x2=443.0, y2=193.0, stroke="#C36A6A", stroke_dasharray=""),
            CircleSlot(id="slot.figure.right.head", prompt="", cx=657.0, cy=188.0, r=22.0, fill="#F3C0AD"),
            RectSlot(id="slot.figure.right.body", prompt="", x=646.0, y=204.0, width=22.0, height=30.0, rx=8.0, ry=8.0, fill="#F2C66D", stroke="#F2C66D"),
            CircleSlot(id="slot.figure.right.eye1", prompt="", cx=651.0, cy=184.0, r=2.5, fill="#222222"),
            CircleSlot(id="slot.figure.right.eye2", prompt="", cx=663.0, cy=184.0, r=2.5, fill="#222222"),
            LineSlot(id="slot.figure.right.mouth", prompt="", x1=651.0, y1=193.0, x2=663.0, y2=193.0, stroke="#C36A6A", stroke_dasharray=""),
            TextSlot(id="slot.name.left", prompt="", text="은우", style_role="choice", x=205.0, y=234.0, font_size=28),
            TextSlot(id="slot.name.mid", prompt="", text="상환", style_role="choice", x=426.0, y=234.0, font_size=28),
            TextSlot(id="slot.name.right", prompt="", text="기영", style_role="choice", x=646.0, y=234.0, font_size=28),
            TextSlot(id="slot.a4", prompt="", text="몫이 다른 사람은 상환입니다.", style_role="body", x=58.0, y=366.0, font_size=28),
        ),
        diagrams=(), groups=(), constraints=(), tags=("초등", "수학", "나눗셈", "몫", "비교"),
    )

PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE={"problem_id":"S3_초등_3_008608","problem_type":"selection_by_division_result","metadata":{"language":"ko","question":"몫이 다른 사람을 선택해 보세요.","instruction":"세 사람의 나눗셈 결과를 비교해 몫이 다른 사람을 고르세요."},"domain":{"objects":[{"id":"obj.person.1","type":"person","name":"은우"},{"id":"obj.person.2","type":"person","name":"상환"},{"id":"obj.person.3","type":"person","name":"기영"},{"id":"obj.expr.1","type":"division_expression","text":"30 ÷ 3"},{"id":"obj.expr.2","type":"division_expression","text":"40 ÷ 2"},{"id":"obj.expr.3","type":"division_expression","text":"70 ÷ 7"}],"relations":[],"problem_solving":{"understand":{"given_refs":["obj.expr.1","obj.expr.2","obj.expr.3"],"target_ref":"answer.target","condition_refs":["rel.select_other"]},"plan":{"method":"compare_results","description":"각 나눗셈의 몫을 구해 다른 값을 가진 사람을 고른다."},"execute":{"expected_operations":["compute_division_results","compare_values","select_unique_person"]},"review":{"check_methods":["same_result_group_check","unique_result_check"]}}},"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"selected_person","description":"몫이 다른 사람"},"value":"상환","unit":""}}
SOLVABLE={"schema":"modu.solvable.v1.1","problem_id":"S3_초등_3_008608","problem_type":"selection_by_division_result","inputs":{"total_ticks":3,"target_label":"몫이 다른 사람","target_ticks":1,"target_count":1,"unit":""},"given":[{"ref":"obj.expr.1","value":{"text":"30 ÷ 3"}},{"ref":"obj.expr.2","value":{"text":"40 ÷ 2"}},{"ref":"obj.expr.3","value":{"text":"70 ÷ 7"}}],"target":{"ref":"answer.target","type":"selected_person"},"method":"compare_results","plan":["세 식의 몫을 구한다.","몫이 다른 값을 찾는다.","해당 사람을 선택한다."],"steps":[{"id":"step.1","expr":"30 ÷ 3","value":10},{"id":"step.2","expr":"40 ÷ 2","value":20},{"id":"step.3","expr":"70 ÷ 7","value":10},{"id":"step.4","expr":"다른 몫의 사람","value":"상환"}],"checks":[{"id":"check.1","expr":"10,20,10 비교","expected":"상환","actual":"상환","pass":True}],"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"selected_person","description":"몫이 다른 사람"},"value":"상환","unit":""}}
