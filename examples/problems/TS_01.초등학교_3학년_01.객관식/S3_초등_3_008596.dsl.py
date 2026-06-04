from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008596",
        title="문제를 바르게 설명한 사람의 이름을 선택해 보세요.",
        canvas=Canvas(width=728.0, height=595.0, coordinate_mode="logical"),
        regions=(Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q.number","slot.q.text","slot.box","slot.box.text","slot.bubble.left","slot.bubble.right","slot.bubble.left.text","slot.bubble.right.text","slot.character.left.head","slot.character.left.body","slot.character.left.eye1","slot.character.left.eye2","slot.character.left.mouth","slot.character.right.head","slot.character.right.body","slot.character.right.eye1","slot.character.right.eye2","slot.character.right.mouth","slot.name.left","slot.name.right","slot.choice")),),
        slots=(
            TextSlot(id="slot.q.number", prompt="", text="65.", style_role="question", x=30.0, y=31.0, font_size=28),
            TextSlot(id="slot.q.text", prompt="", text="문제를 바르게 설명한 사람의 이름을 선택해 보세요.", style_role="question", x=76.0, y=31.0, font_size=28),
            RectSlot(id="slot.box", prompt="", x=384.0, y=48.0, width=188.0, height=63.0),
            TextSlot(id="slot.box.text", prompt="", text="83 ÷ 6", style_role="choice", x=436.0, y=92.0, font_size=28),
            RectSlot(id="slot.bubble.left", prompt="", x=285.0, y=127.0, width=121.0, height=81.0),
            RectSlot(id="slot.bubble.right", prompt="", x=530.0, y=127.0, width=158.0, height=95.0),
            TextSlot(id="slot.bubble.left.text", prompt="", text="몫은 13이야.", style_role="question", x=311.0, y=170.0, font_size=28),
            TextSlot(id="slot.bubble.right.text", prompt="", text="나머지는 0으로\n나누어떨어져.", style_role="question", x=554.0, y=165.0, font_size=28),
            CircleSlot(id="slot.character.left.head", prompt="", cx=336.0, cy=272.0, r=24.0, fill="#F3C0AD"),
            RectSlot(id="slot.character.left.body", prompt="", x=324.0, y=288.0, width=24.0, height=34.0, rx=8.0, ry=8.0, fill="#D7A0D7", stroke="#D7A0D7"),
            CircleSlot(id="slot.character.left.eye1", prompt="", cx=330.0, cy=268.0, r=2.5, fill="#222222"),
            CircleSlot(id="slot.character.left.eye2", prompt="", cx=342.0, cy=268.0, r=2.5, fill="#222222"),
            LineSlot(id="slot.character.left.mouth", prompt="", x1=330.0, y1=278.0, x2=342.0, y2=278.0, stroke="#C36A6A", stroke_dasharray=""),
            CircleSlot(id="slot.character.right.head", prompt="", cx=611.0, cy=275.0, r=24.0, fill="#F3C0AD"),
            RectSlot(id="slot.character.right.body", prompt="", x=599.0, y=291.0, width=24.0, height=34.0, rx=8.0, ry=8.0, fill="#8ED7E6", stroke="#8ED7E6"),
            CircleSlot(id="slot.character.right.eye1", prompt="", cx=605.0, cy=271.0, r=2.5, fill="#222222"),
            CircleSlot(id="slot.character.right.eye2", prompt="", cx=617.0, cy=271.0, r=2.5, fill="#222222"),
            LineSlot(id="slot.character.right.mouth", prompt="", x1=605.0, y1=281.0, x2=617.0, y2=281.0, stroke="#C36A6A", stroke_dasharray=""),
            TextSlot(id="slot.name.left", prompt="", text="종우", style_role="question", x=318.0, y=396.0, font_size=28),
            TextSlot(id="slot.name.right", prompt="", text="은아", style_role="question", x=594.0, y=396.0, font_size=28),
            TextSlot(id="slot.choice", prompt="", text="( 종우 , 은아 )", style_role="question", x=416.0, y=428.0, font_size=28),
        ),
        diagrams=(), groups=(), constraints=(), tags=("초등","수학","나눗셈","몫","나머지","선택형"),
    )

PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE={"problem_id":"S3_초등_3_008596","problem_type":"division_quotient_remainder_choice","metadata":{"language":"ko","question":"문제를 바르게 설명한 사람의 이름을 선택해 보세요.","instruction":"나눗셈의 몫과 나머지를 바르게 설명한 사람을 고르세요."},"domain":{"objects":[{"id":"obj.dividend","type":"number","value":83},{"id":"obj.divisor","type":"number","value":6},{"id":"obj.person.jongwoo","type":"person","name":"종우"},{"id":"obj.person.eunah","type":"person","name":"은아"}],"relations":[],"problem_solving":{"understand":{"given_refs":["obj.dividend","obj.divisor","obj.person.jongwoo","obj.person.eunah"],"target_ref":"answer.target","condition_refs":["rel.division_statement","rel.correct_explainer"]},"plan":{"method":"quotient_remainder_check","description":"나눗셈의 몫과 나머지 설명이 맞는 사람을 고른다."},"execute":{"expected_operations":["interpret_division_expression","compare_explanations","select_correct_person"]},"review":{"check_methods":["quotient_remainder_consistency"]}}},"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"person_name","description":"문제를 바르게 설명한 사람의 이름"},"value":"종우","unit":""}}
SOLVABLE={"schema":"modu.solvable.v1.1","problem_id":"S3_초등_3_008596","problem_type":"division_quotient_remainder_choice","inputs":{"total_ticks":1,"target_label":"문제를 바르게 설명한 사람의 이름","target_ticks":1,"target_count":1,"unit":""},"given":[{"ref":"obj.dividend","value":83},{"ref":"obj.divisor","value":6},{"ref":"obj.person.jongwoo","value":{"name":"종우"}},{"ref":"obj.person.eunah","value":{"name":"은아"}}],"target":{"ref":"answer.target","type":"person_name"},"method":"quotient_remainder_check","plan":["83 ÷ 6의 몫과 나머지를 구한다.","두 사람의 설명과 실제 값을 비교한다.","맞는 사람의 이름을 고른다."],"steps":[{"id":"step.1","expr":"83 ÷ 6","value":{"quotient":13,"remainder":5}},{"id":"step.2","expr":"설명 비교","value":"종우"}],"checks":[{"id":"check.1","expr":"83 = 6 × 13 + 5","expected":True,"actual":True,"pass":True}],"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"person_name","description":"문제를 바르게 설명한 사람의 이름"},"value":"종우","unit":""}}
