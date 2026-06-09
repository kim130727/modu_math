from __future__ import annotations
from modu_math.dsl import Canvas, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot

def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008576",
        title="색칠된 부분은 실제 어떤 수의 곱인지를 찾아 선택하세요.",
        canvas=Canvas(width=900, height=420, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q.text")),
            Region(id="region.work", role="diagram", flow="absolute", slot_ids=()),
            Region(id="region.choice", role="choices", flow="absolute", slot_ids=()),
            Region(id="region.footer", role="footer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(id="slot.q.text", prompt="", text="색칠된 부분은 실제 어떤 수의 곱인지를 찾아 선택하세요.", style_role="question", x = 40, y = 40, font_size=36),

            LineSlot(id="slot.v1", prompt="", x1 = 425, y1 = 60, x2 = 425, y2 = 250, stroke="#9AA0A6", stroke_width=1.2, stroke_dasharray="5 3"),
            LineSlot(id="slot.v2", prompt="", x1 = 465, y1 = 60, x2 = 465, y2 = 250, stroke="#9AA0A6", stroke_width=1.2, stroke_dasharray="5 3"),
            LineSlot(id="slot.v3", prompt="", x1 = 505, y1 = 60, x2 = 505, y2 = 250, stroke="#9AA0A6", stroke_width=1.2, stroke_dasharray="5 3"),
            LineSlot(id="slot.v4", prompt="", x1 = 545, y1 = 60, x2 = 545, y2 = 250, stroke="#9AA0A6", stroke_width=1.2, stroke_dasharray="5 3"),
            LineSlot(id="slot.v5", prompt="", x1 = 585, y1 = 60, x2 = 585, y2 = 250, stroke="#9AA0A6", stroke_width=1.2, stroke_dasharray="5 3"),

            TextSlot(id="slot.top2", prompt="", text = '5 9 3', style_role="diagram", x = 480, y = 95, font_size = 45),
            TextSlot(id="slot.mulx", prompt="", text="×", style_role="diagram", x = 425, y = 135, font_size=44),
            TextSlot(id="slot.mul0", prompt="", text="2", style_role="diagram", x = 555, y = 135, font_size=44),
            LineSlot(id="slot.bar1", prompt="", x1 = 415, y1 = 140, x2 = 585, y2 = 140),

            RectSlot(id="slot.hl1", prompt="", x = 550, y = 100, width = 40, height = 40, fill="#efc8b9"),
            RectSlot(id="slot.hl2", prompt="", x = 510, y = 60, width = 40, height = 40, fill="#efc8b9"),

            RectSlot(id="slot.choice.box", prompt="", x = 40, y = 335, width = 835, height = 75, stroke="#D8A100", stroke_width=2.0, fill="none"),
            TextSlot(id="slot.c1", prompt="", text = '90 × 20', style_role="choice", x = 120, y = 385, font_size = 40),
            TextSlot(id="slot.c2", prompt="", text = '9 × 2', style_role="choice", x = 315, y = 385, font_size = 40),
            TextSlot(id="slot.c3", prompt="", text = '90 × 2', style_role="choice", x = 470, y = 385, font_size = 40),
            TextSlot(id="slot.c4", prompt="", text = '900 × 2', style_role="choice", x = 645, y = 385, font_size = 40),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등", "수학", "곱셈", "세로셈", "자리값"),
    )

PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE={"problem_id":"S3_초등_3_008577","problem_type":"multiplication_place_value_choice","metadata":{"language":"ko","question":"색칠된 부분은 실제 어떤 수의 곱인지를 찾아 선택하세요.","instruction":"보기에서 알맞은 식을 고르세요."},"domain":{"objects":[{"id":"obj.target","type":"expression","text":"90 × 2"}],"relations":[]},"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"selected_expression","description":"색칠된 부분에 해당하는 식"},"value":"90 × 2","unit":""}}
SOLVABLE={"schema":"modu.solvable.v1.1","problem_id":"S3_초등_3_008577","problem_type":"multiplication_place_value_choice","inputs":{"total_ticks":0,"target_label":"색칠된 부분에 해당하는 식","target_ticks":0,"target_count":1,"unit":""},"given":[{"ref":"obj.target","value":"90 × 2"}],"target":{"ref":"answer.target","type":"selected_expression"},"method":"place_value_matching","plan":["색칠된 부분과 자리값을 확인한다.","같은 식을 고른다."],"steps":[{"id":"step.1","expr":"색칠된 부분과 보기 비교","value":"90 × 2"}],"checks":[{"id":"check.1","expr":"검토","expected":"일치","actual":"일치","pass":True}],"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"selected_expression","description":"색칠된 부분에 해당하는 식"},"value":"90 × 2","unit":""}}
