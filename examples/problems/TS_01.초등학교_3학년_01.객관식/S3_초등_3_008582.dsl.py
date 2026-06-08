from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot, character_body_slot_ids, character_body_slots, character_hand_slot_ids, character_hand_slots


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008582",
        title="계산 결과가 더 큰 사람의 이름을 선택해 보세요.",
        canvas=Canvas(width=766.0, height=396.0, coordinate_mode="logical"),
        regions=(
            Region(id="region.header", role="stem", flow="absolute", slot_ids=("slot.q_text",)),
            Region(
                id="region.left",
                role="content",
                flow="absolute",
                slot_ids=(
                    *character_body_slot_ids("slot.person_left"),
                    "slot.name_left_box",
                    "slot.name_left",
                    "slot.card_left",
                    *character_hand_slot_ids("slot.person_left"),
                    "slot.card_left_text",
                ),
            ),
            Region(
                id="region.right",
                role="content",
                flow="absolute",
                slot_ids=(
                    *character_body_slot_ids("slot.person_right", glasses=True),
                    "slot.name_right_box",
                    "slot.name_right",
                    "slot.card_right",
                    *character_hand_slot_ids("slot.person_right"),
                    "slot.card_right_text",
                ),
            ),
        ),
        slots=(
            TextSlot(id="slot.q_text", prompt="", text="계산 결과가 더 큰 사람의 이름을 선택해 보세요.", style_role="question", x=60.0, y=37.0, font_size=28),
            *character_body_slots("slot.person_left", cx=367, head_cy=97, hair="#4b1f16", shirt="#d28bc8"),
            RectSlot(id="slot.name_left_box", prompt="", x = 207, y = 116, width = 70, height = 38, rx=8, ry=8, stroke="#b8c7dc", stroke_width=1.8, fill="#ffffff"),
            TextSlot(id="slot.name_left", prompt="", text = '진수', style_role="label", x = 222, y = 143, font_size = 25),
            RectSlot(id="slot.card_left", prompt="", x = 306, y = 136, width = 130, height = 59, fill="#F6C344"),
            *character_hand_slots("slot.person_left", card_x=306, card_y=136, card_width=130),
            TextSlot(id="slot.card_left_text", prompt="", text = '63 × 12', style_role="math", x = 330, y = 171, font_size = 25),

            *character_body_slots("slot.person_right", cx=582, head_cy=97, hair="#1d1714", shirt="#e85d50", glasses=True),
            RectSlot(id="slot.name_right_box", prompt="", x = 676, y = 112, width = 72, height = 38, rx=8, ry=8, stroke="#b8c7dc", stroke_width=1.8, fill="#ffffff"),
            TextSlot(id="slot.name_right", prompt="", text = '수호', style_role="label", x = 690, y = 139, font_size = 25),
            RectSlot(id="slot.card_right", prompt="", x = 522, y = 136, width = 130, height = 59, fill="#F6C344"),
            *character_hand_slots("slot.person_right", card_x=522, card_y=136, card_width=130),
            TextSlot(id="slot.card_right_text", prompt="", text = '24 × 31', style_role="math", x = 545, y = 171, font_size = 25),
        ),
        diagrams=(), groups=(), constraints=(), tags=("초등", "수학", "곱셈", "비교", "선택형"),
    )

PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE={"problem_id":"S3_초등_3_008582","problem_type":"comparison_selection","metadata":{"language":"ko","question":"계산 결과가 더 큰 사람의 이름을 선택해 보세요.","instruction":"두 사람의 곱셈 결과를 비교하여 더 큰 사람을 고르세요."},"domain":{"objects":[{"id":"obj.person.jinsu","type":"person","name":"진수"},{"id":"obj.person.suho","type":"person","name":"수호"},{"id":"obj.expr.jinsu","type":"multiplication_expression","expression":"63 × 12"},{"id":"obj.expr.suho","type":"multiplication_expression","expression":"24 × 31"}],"relations":[],"problem_solving":{"understand":{"given_refs":["obj.person.jinsu","obj.person.suho","obj.expr.jinsu","obj.expr.suho"],"target_ref":"answer.target","condition_refs":["rel.compare.results"]},"plan":{"method":"compute_and_compare","description":"곱셈 결과를 구해 큰 값을 가진 사람을 고른다."},"execute":{"expected_operations":["multiply","compare_results","select_name"]},"review":{"check_methods":["compare_computed_values"]}}},"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"person_name","description":"계산 결과가 더 큰 사람의 이름"},"value":"진수","unit":""}}
SOLVABLE={"schema":"modu.solvable.v1.1","problem_id":"S3_초등_3_008582","problem_type":"comparison_selection","inputs":{"total_ticks":2,"target_label":"더 큰 계산 결과를 가진 사람의 이름","target_ticks":1,"target_count":1,"unit":""},"given":[{"ref":"obj.expr.jinsu","value":"63 × 12"},{"ref":"obj.expr.suho","value":"24 × 31"}],"target":{"ref":"answer.target","type":"person_name"},"method":"compute_and_compare","plan":["각 곱셈식을 계산한다.","두 결과를 비교한다.","더 큰 결과의 이름을 고른다."],"steps":[{"id":"step.1","expr":"63 × 12","value":756},{"id":"step.2","expr":"24 × 31","value":744},{"id":"step.3","expr":"756 > 744","value":True},{"id":"step.4","expr":"더 큰 결과의 이름 선택","value":"진수"}],"checks":[{"id":"check.1","expr":"63 × 12 = 756","expected":756,"actual":756,"pass":True},{"id":"check.2","expr":"24 × 31 = 744","expected":744,"actual":744,"pass":True}],"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"person_name","description":"계산 결과가 더 큰 사람의 이름"},"value":"진수","unit":""}}
