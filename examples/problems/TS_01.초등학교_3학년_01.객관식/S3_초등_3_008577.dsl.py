from __future__ import annotations
from modu_math.dsl import Canvas, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot

def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(id="S3_??_3_008577", title="색칠된 부분은 실제 어떤 수의 곱인지를 찾아 선택하세요.", canvas=Canvas(width=900,height=420,coordinate_mode="logical"),
    regions=(Region(id="region.stem",role="stem",flow="absolute",slot_ids=("slot.q.no","slot.q.text")),),
    slots=(
    TextSlot(id="slot.q.no",prompt="",text="43.",style_role="question",x=12,y=30,font_size=38),
    TextSlot(id="slot.q.text",prompt="",text="색칠된 부분은 실제 어떤 수의 곱인지를 찾아 선택하세요.",style_role="question",x=48,y=30,font_size=44),
    RectSlot(id="slot.choice.box",prompt="",x=513,y=63,width=150,height=219,fill="none"),
    RectSlot(id="slot.hl1",prompt="",x=367,y=122,width=30,height=30,fill="#c8d8cc"),
    RectSlot(id="slot.hl2",prompt="",x=396,y=162,width=34,height=40,fill="#c8d8cc"),
    TextSlot(id="slot.t2",prompt="",text="5",style_role="diagram",x=344,y=154,font_size=44),
    TextSlot(id="slot.t1",prompt="",text="9",style_role="diagram",x=384,y=154,font_size=44),
    TextSlot(id="slot.t0",prompt="",text="3",style_role="diagram",x=424,y=154,font_size=44),
    TextSlot(id="slot.mx",prompt="",text="?",style_role="diagram",x=314,y=195,font_size=44),
    TextSlot(id="slot.m0",prompt="",text="2",style_role="diagram",x=424,y=196,font_size=44),
    LineSlot(id="slot.l",prompt="",x1=300,y1=202,x2=436,y2=202),
    TextSlot(id="slot.c1",prompt="",text="90 ? 20",style_role="choice",x=536,y=112,font_size=40),
    TextSlot(id="slot.c2",prompt="",text="9 ? 2",style_role="choice",x=552,y=154,font_size=40),
    TextSlot(id="slot.c3",prompt="",text="900 ? 2",style_role="choice",x=536,y=196,font_size=40),
    TextSlot(id="slot.c4",prompt="",text="90 ? 2",style_role="choice",x=552,y=238,font_size=40),
    TextSlot(id="slot.a",prompt="",text="(??)90 ? 2",style_role="body",x=8,y=334,font_size=36),
    TextSlot(id="slot.e",prompt="",text="(??)593?? 9? ?? ?? ????? 90 ? 2 = 180???.",style_role="body",x=8,y=382,font_size=40),
    ),diagrams=(),groups=(),constraints=(),tags=("??","??","??"))
PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE={"problem_id":"S3_??_3_008577","problem_type":"multiplication_place_value_choice","metadata":{"language":"ko","question":"색칠된 부분은 실제 어떤 수의 곱인지를 찾아 선택하세요.","instruction":"???? ??? ?? ????."},"domain":{"objects":[{"id":"obj.target","type":"expression","text":"90 ? 2"}],"relations":[]},"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"selected_expression","description":"??? ??? ???? ?"},"value":"90 ? 2","unit":""}}
SOLVABLE={"schema":"modu.solvable.v1.1","problem_id":"S3_??_3_008577","problem_type":"multiplication_place_value_choice","inputs":{"total_ticks":0,"target_label":"??? ??? ???? ?","target_ticks":0,"target_count":1,"unit":""},"given":[{"ref":"obj.target","value":"90 ? 2"}],"target":{"ref":"answer.target","type":"selected_expression"},"method":"place_value_matching","plan":["??? ??? ???? ????.","?? ?? ???."],"steps":[{"id":"step.1","expr":"??? ??? ?? ??","value":"90 ? 2"}],"checks":[{"id":"check.1","expr":"??","expected":"??","actual":"??","pass":True}],"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"selected_expression","description":"??? ??? ???? ?"},"value":"90 ? 2","unit":""}}
