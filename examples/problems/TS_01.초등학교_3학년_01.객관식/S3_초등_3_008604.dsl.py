from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, LineSlot, PathSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008604",
        title="문제를 바르게 설명한 사람의 이름을 선택하세요.",
        canvas=Canvas(width=785.0, height=559.0, coordinate_mode="logical"),
        regions=(Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1","slot.expr_box","slot.expr_text","slot.bubble_left","slot.bubble_right","slot.bubble_left_text","slot.bubble_right_text","slot.face_left.head","slot.face_left.body","slot.face_left.eye1","slot.face_left.eye2","slot.face_left.mouth","slot.face_right.head","slot.face_right.body","slot.face_right.eye1","slot.face_right.eye2","slot.face_right.mouth","slot.name_left","slot.name_right","slot.choice")),),
        slots=(
            TextSlot(id="slot.q1", prompt="", text="74. 문제를 바르게 설명한 사람의 이름을 선택하세요.", style_role="question", x=12.0, y=28.0, font_size=28),
            RectSlot(id="slot.expr_box", prompt="", x=390.0, y=41.0, width=186.0, height=62.0, fill="none", stroke="#F4A340", stroke_width=2.0),
            TextSlot(id="slot.expr_text", prompt="", text="67 ÷ 5", style_role="choice", x=442.0, y=84.0, font_size=28),
            PathSlot(id="slot.bubble_left", prompt="", d="M 238.0 189.0 C 214.0 180.0 194.0 170.0 187.0 154.0 C 182.0 141.0 187.0 125.0 202.0 114.0 C 219.0 101.0 244.0 98.0 269.0 103.0 C 294.0 108.0 312.0 120.0 317.0 136.0 C 322.0 151.0 315.0 166.0 300.0 175.0 C 289.0 182.0 275.0 186.0 261.0 187.0 L 249.0 225.0 Z", fill="white", stroke="#888888", stroke_width=1.2),
            PathSlot(id="slot.bubble_right", prompt="", d="M 641.0 240.0 C 620.0 234.0 603.0 223.0 595.0 208.0 C 588.0 193.0 592.0 176.0 606.0 164.0 C 620.0 151.0 642.0 145.0 666.0 147.0 C 692.0 149.0 712.0 159.0 720.0 175.0 C 728.0 190.0 724.0 207.0 709.0 219.0 C 696.0 229.0 680.0 235.0 663.0 237.0 L 653.0 277.0 Z", fill="white", stroke="#888888", stroke_width=1.2),
            TextSlot(id="slot.bubble_left_text", prompt="", text="몫은 13이야.", style_role="question", x=241.0, y=160.0, font_size=28),
            TextSlot(id="slot.bubble_right_text", prompt="", text="나머지는 0으로\n나누어떨어져.", style_role="question", x=619.0, y=185.0, font_size=28),
            CircleSlot(id="slot.face_left.head", prompt="", cx=333.0, cy=292.0, r=32.0, fill="#F3C0AD"),
            RectSlot(id="slot.face_left.body", prompt="", x=317.0, y=313.0, width=32.0, height=40.0, rx=10.0, ry=10.0, fill="#D7A0D7", stroke="#D7A0D7"),
            CircleSlot(id="slot.face_left.eye1", prompt="", cx=325.0, cy=288.0, r=3.0, fill="#222222"),
            CircleSlot(id="slot.face_left.eye2", prompt="", cx=341.0, cy=288.0, r=3.0, fill="#222222"),
            LineSlot(id="slot.face_left.mouth", prompt="", x1=326.0, y1=300.0, x2=340.0, y2=300.0, stroke="#C36A6A", stroke_dasharray=""),
            CircleSlot(id="slot.face_right.head", prompt="", cx=633.0, cy=304.0, r=32.0, fill="#F3C0AD"),
            RectSlot(id="slot.face_right.body", prompt="", x=617.0, y=325.0, width=32.0, height=40.0, rx=10.0, ry=10.0, fill="#8ED7E6", stroke="#8ED7E6"),
            CircleSlot(id="slot.face_right.eye1", prompt="", cx=625.0, cy=300.0, r=3.0, fill="#222222"),
            CircleSlot(id="slot.face_right.eye2", prompt="", cx=641.0, cy=300.0, r=3.0, fill="#222222"),
            LineSlot(id="slot.face_right.mouth", prompt="", x1=626.0, y1=312.0, x2=640.0, y2=312.0, stroke="#C36A6A", stroke_dasharray=""),
            TextSlot(id="slot.name_left", prompt="", text="현태", style_role="question", x=313.0, y=389.0, font_size=28),
            TextSlot(id="slot.name_right", prompt="", text="은수", style_role="question", x=618.0, y=389.0, font_size=28),
            TextSlot(id="slot.choice", prompt="", text="( 현태 , 은수 )", style_role="question", x=411.0, y=420.0, font_size=28),
        ),
        diagrams=(), groups=(), constraints=(), tags=("초등","수학","나눗셈","몫","나머지","선택형"),
    )

PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE={"problem_id":"S3_초등_3_008604","problem_type":"division_reasoning_multiple_choice","metadata":{"language":"ko","question":"67 ÷ 5의 결과를 바르게 설명한 사람을 고르는 문제","instruction":"문제를 바르게 설명한 사람의 이름을 선택하세요."},"domain":{"objects":[{"id":"obj.dividend","type":"number","value":67},{"id":"obj.divisor","type":"number","value":5},{"id":"obj.speaker.left","type":"person","name":"현태"},{"id":"obj.speaker.right","type":"person","name":"은수"}],"relations":[],"problem_solving":{"understand":{"given_refs":["obj.dividend","obj.divisor","obj.speaker.left","obj.speaker.right"],"target_ref":"answer.target","condition_refs":["rel.division","rel.left_statement","rel.right_statement"]},"plan":{"method":"division_reasoning","description":"나눗셈의 몫과 나머지 설명이 맞는지 비교한다."},"execute":{"expected_operations":["interpret_quotient_statement","interpret_remainder_statement","compare_with_division_result"]},"review":{"check_methods":["statement_match_check","division_consistency_check"]}}},"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"person_name","description":"문제를 바르게 설명한 사람의 이름"},"value":"현태","unit":""}}
SOLVABLE={"schema":"modu.solvable.v1.1","problem_id":"S3_초등_3_008604","problem_type":"division_reasoning_multiple_choice","inputs":{"total_ticks":0,"target_label":"문제를 바르게 설명한 사람의 이름","target_ticks":0,"target_count":1,"unit":""},"given":[{"ref":"obj.dividend","value":67},{"ref":"obj.divisor","value":5},{"ref":"obj.speaker.left","value":"현태"},{"ref":"obj.speaker.right","value":"은수"}],"target":{"ref":"answer.target","type":"person_name"},"method":"division_reasoning","plan":["나눗셈의 몫과 나머지 설명을 비교한다.","문장 내용이 67 ÷ 5의 결과와 맞는지 확인한다."],"steps":[{"id":"step.1","expr":"67 ÷ 5의 몫과 나머지를 해설 표기와 비교","value":{"quotient_statement":"몫은 13이야.","remainder_statement":"나머지는 0으로 나누어떨어져."}},{"id":"step.2","expr":"실제 계산 결과와 비교","value":{"quotient":13,"remainder":2}},{"id":"step.3","expr":"문제를 바르게 설명한 사람 선택","value":"현태"}],"checks":[{"id":"check.1","expr":"몫 설명이 13인지 확인","expected":True,"actual":True,"pass":True},{"id":"check.2","expr":"나머지 설명이 0이 아닌지 확인","expected":True,"actual":True,"pass":True}],"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"person_name","description":"문제를 바르게 설명한 사람의 이름"},"value":"현태","unit":""}}
