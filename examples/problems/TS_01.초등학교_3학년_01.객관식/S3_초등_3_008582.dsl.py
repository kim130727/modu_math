from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008582",
        title="계산 결과가 더 큰 사람의 이름을 선택해 보세요.",
        canvas=Canvas(width=766.0, height=396.0, coordinate_mode="logical"),
        regions=(
            Region(id="region.header", role="stem", flow="absolute", slot_ids=("slot.q_num", "slot.q_text")),
            Region(id="region.left", role="content", flow="absolute", slot_ids=("slot.name_left", "slot.card_left", "slot.card_left_text", "slot.face_left.head", "slot.face_left.body", "slot.face_left.eye1", "slot.face_left.eye2", "slot.face_left.mouth")),
            Region(id="region.right", role="content", flow="absolute", slot_ids=("slot.name_right", "slot.card_right", "slot.card_right_text", "slot.face_right.head", "slot.face_right.body", "slot.face_right.eye1", "slot.face_right.eye2", "slot.face_right.mouth")),
        ),
        slots=(
            TextSlot(id="slot.q_num", prompt="", text="48.", style_role="question", x=12.0, y=37.0, font_size=28),
            TextSlot(id="slot.q_text", prompt="", text="계산 결과가 더 큰 사람의 이름을 선택해 보세요.", style_role="question", x=60.0, y=37.0, font_size=28),
            CircleSlot(id="slot.face_left.head", prompt="", cx=230.0, cy=88.0, r=20.0, fill="#F3C0AD"),
            RectSlot(id="slot.face_left.body", prompt="", x=220.0, y=102.0, width=20.0, height=24.0, rx=8.0, ry=8.0, fill="#D7A0D7", stroke="#D7A0D7"),
            CircleSlot(id="slot.face_left.eye1", prompt="", cx=225.0, cy=85.0, r=2.0, fill="#222222"),
            CircleSlot(id="slot.face_left.eye2", prompt="", cx=235.0, cy=85.0, r=2.0, fill="#222222"),
            LineSlot(id="slot.face_left.mouth", prompt="", x1=225.0, y1=92.0, x2=235.0, y2=92.0, stroke="#C36A6A", stroke_dasharray=""),
            TextSlot(id="slot.name_left", prompt="", text="진수", style_role="label", x=200.0, y=126.0, font_size=28),
            RectSlot(id="slot.card_left", prompt="", x=170.0, y=140.0, width=129.0, height=64.0, fill="#F6C344"),
            TextSlot(id="slot.card_left_text", prompt="", text="63 × 12", style_role="math", x=180.0, y=180.0, font_size=28),

            CircleSlot(id="slot.face_right.head", prompt="", cx=430.0, cy=88.0, r=20.0, fill="#F3C0AD"),
            RectSlot(id="slot.face_right.body", prompt="", x=420.0, y=102.0, width=20.0, height=24.0, rx=8.0, ry=8.0, fill="#8ED7E6", stroke="#8ED7E6"),
            CircleSlot(id="slot.face_right.eye1", prompt="", cx=425.0, cy=85.0, r=2.0, fill="#222222"),
            CircleSlot(id="slot.face_right.eye2", prompt="", cx=435.0, cy=85.0, r=2.0, fill="#222222"),
            LineSlot(id="slot.face_right.mouth", prompt="", x1=425.0, y1=92.0, x2=435.0, y2=92.0, stroke="#C36A6A", stroke_dasharray=""),
            TextSlot(id="slot.name_right", prompt="", text="수호", style_role="label", x=400.0, y=126.0, font_size=28),
            RectSlot(id="slot.card_right", prompt="", x=365.0, y=140.0, width=129.0, height=64.0, fill="#F6C344"),
            TextSlot(id="slot.card_right_text", prompt="", text="24 × 31", style_role="math", x=380.0, y=180.0, font_size=28),
        ),
        diagrams=(), groups=(), constraints=(), tags=("초등", "수학", "곱셈", "비교", "선택형"),
    )

PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE={"problem_id":"S3_초등_3_008582","problem_type":"comparison_selection","metadata":{"language":"ko","question":"계산 결과가 더 큰 사람의 이름을 선택해 보세요.","instruction":"두 사람의 곱셈 결과를 비교하여 더 큰 사람을 고르세요."},"domain":{"objects":[{"id":"obj.person.jinsu","type":"person","name":"진수"},{"id":"obj.person.suho","type":"person","name":"수호"},{"id":"obj.expr.jinsu","type":"multiplication_expression","expression":"63 × 12"},{"id":"obj.expr.suho","type":"multiplication_expression","expression":"24 × 31"}],"relations":[],"problem_solving":{"understand":{"given_refs":["obj.person.jinsu","obj.person.suho","obj.expr.jinsu","obj.expr.suho"],"target_ref":"answer.target","condition_refs":["rel.compare.results"]},"plan":{"method":"compute_and_compare","description":"곱셈 결과를 구해 큰 값을 가진 사람을 고른다."},"execute":{"expected_operations":["multiply","compare_results","select_name"]},"review":{"check_methods":["compare_computed_values"]}}},"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"person_name","description":"계산 결과가 더 큰 사람의 이름"},"value":"진수","unit":""}}
SOLVABLE={"schema":"modu.solvable.v1.1","problem_id":"S3_초등_3_008582","problem_type":"comparison_selection","inputs":{"total_ticks":2,"target_label":"더 큰 계산 결과를 가진 사람의 이름","target_ticks":1,"target_count":1,"unit":""},"given":[{"ref":"obj.expr.jinsu","value":"63 × 12"},{"ref":"obj.expr.suho","value":"24 × 31"}],"target":{"ref":"answer.target","type":"person_name"},"method":"compute_and_compare","plan":["각 곱셈식을 계산한다.","두 결과를 비교한다.","더 큰 결과의 이름을 고른다."],"steps":[{"id":"step.1","expr":"63 × 12","value":756},{"id":"step.2","expr":"24 × 31","value":744},{"id":"step.3","expr":"756 > 744","value":True},{"id":"step.4","expr":"더 큰 결과의 이름 선택","value":"진수"}],"checks":[{"id":"check.1","expr":"63 × 12 = 756","expected":756,"actual":756,"pass":True},{"id":"check.2","expr":"24 × 31 = 744","expected":744,"actual":744,"pass":True}],"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"person_name","description":"계산 결과가 더 큰 사람의 이름"},"value":"진수","unit":""}}
