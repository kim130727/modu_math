from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, SpeakerSpec, TextSlot, speaker_group_slot_ids, speaker_group_slots


def build_problem_template() -> ProblemTemplate:
    speakers = (
        SpeakerSpec(
            key="left",
            cx = ((345.5) + (-105.0)) + (5.0), bubble_cy = ((167.5) + (15.0)) + (-5.0), head_cy = ((272.0) + (15.0)) + (-5.0), text="몫은 13이야.",
            name="종우",
            hair="#4b1f16",
            shirt="#D7A0D7",
            bubble_width=140.0,
            bubble_height=81.0,
            name_width=76.0,
            name_y = ((370.0) + (15.0)) + (-5.0), speech_font_size=24,
            speech_text_dy=4,
        ),
        SpeakerSpec(
            key="right",
            cx = ((609.0) + (-145.0)) + (35.0), bubble_cy = ((174.5) + (15.0)) + (-5.0), head_cy = ((275.0) + (15.0)) + (-5.0), text="나머지는 0으로\n나누어떨어져.",
            name="은아",
            hair="#1d1714",
            shirt="#8ED7E6",
            bubble_width=158.0,
            bubble_height=95.0,
            name_width=76.0,
            name_y = ((370.0) + (15.0)) + (-5.0), speech_font_size=22,
            speech_text_dy=-3,
        ),
    )
    return ProblemTemplate(
        id="S3_초등_3_008596",
        title="문제를 바르게 설명한 사람의 이름을 선택해 보세요.",
        canvas=Canvas(width=728.0, height=595.0, coordinate_mode="logical"),
        regions=(Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q.text", "slot.box", "slot.box.text", *speaker_group_slot_ids(speakers), "slot.choice")),),
        slots=(
            TextSlot(id="slot.q.text", prompt="", text="문제를 바르게 설명한 사람의 이름을 선택해 보세요.", style_role="question", x=76.0, y=31.0, font_size=28),
            RectSlot(id="slot.box", prompt="", x = 280, y = 55, width = 190, height = 65),
            TextSlot(id="slot.box.text", prompt="", text = '83 ÷ 6', style_role="choice", x = 320, y = 100, font_size = 30),
            *speaker_group_slots(speakers),
            TextSlot(id="slot.choice", prompt="", text = '( 종우 , 은아 )', style_role="question", x = 280, y = 460, font_size = 30),
        ),
        diagrams=(), groups=(), constraints=(), tags=("초등","수학","나눗셈","몫","나머지","선택형"),
    )

PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE={"problem_id":"S3_초등_3_008596","problem_type":"division_quotient_remainder_choice","metadata":{"language":"ko","question":"문제를 바르게 설명한 사람의 이름을 선택해 보세요.","instruction":"나눗셈의 몫과 나머지를 바르게 설명한 사람을 고르세요."},"domain":{"objects":[{"id":"obj.dividend","type":"number","value":83},{"id":"obj.divisor","type":"number","value":6},{"id":"obj.person.jongwoo","type":"person","name":"종우"},{"id":"obj.person.eunah","type":"person","name":"은아"}],"relations":[],"problem_solving":{"understand":{"given_refs":["obj.dividend","obj.divisor","obj.person.jongwoo","obj.person.eunah"],"target_ref":"answer.target","condition_refs":["rel.division_statement","rel.correct_explainer"]},"plan":{"method":"quotient_remainder_check","description":"나눗셈의 몫과 나머지 설명이 맞는 사람을 고른다."},"execute":{"expected_operations":["interpret_division_expression","compare_explanations","select_correct_person"]},"review":{"check_methods":["quotient_remainder_consistency"]}}},"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"person_name","description":"문제를 바르게 설명한 사람의 이름"},"value":"종우","unit":""}}
SOLVABLE={"schema":"modu.solvable.v1.1","problem_id":"S3_초등_3_008596","problem_type":"division_quotient_remainder_choice","inputs":{"total_ticks":1,"target_label":"문제를 바르게 설명한 사람의 이름","target_ticks":1,"target_count":1,"unit":""},"given":[{"ref":"obj.dividend","value":83},{"ref":"obj.divisor","value":6},{"ref":"obj.person.jongwoo","value":{"name":"종우"}},{"ref":"obj.person.eunah","value":{"name":"은아"}}],"target":{"ref":"answer.target","type":"person_name"},"method":"quotient_remainder_check","plan":["83 ÷ 6의 몫과 나머지를 구한다.","두 사람의 설명과 실제 값을 비교한다.","맞는 사람의 이름을 고른다."],"steps":[{"id":"step.1","expr":"83 ÷ 6","value":{"quotient":13,"remainder":5}},{"id":"step.2","expr":"설명 비교","value":"종우"}],"checks":[{"id":"check.1","expr":"83 = 6 × 13 + 5","expected":True,"actual":True,"pass":True}],"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"person_name","description":"문제를 바르게 설명한 사람의 이름"},"value":"종우","unit":""}}
