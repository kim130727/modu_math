from __future__ import annotations
from modu_math.dsl import Canvas, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot

def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(id="S3_??_3_008575", title="색칠된 부분은 실제 어떤 수의 곱인지를 찾아 선택하세요.", canvas=Canvas(width=900,height=420,coordinate_mode="logical"),
    regions=(Region(id="region.stem",role="stem",flow="absolute",slot_ids=("slot.q.no","slot.q.text")),),
    slots=(
    TextSlot(id="slot.q.no",prompt="",text="41.",style_role="question",x=12,y=30,font_size=38),
    TextSlot(id="slot.q.text",prompt="",text="색칠된 부분은 실제 어떤 수의 곱인지를 찾아 선택하세요.",style_role="question",x=48,y=30,font_size=44),
    RectSlot(id="slot.choice.box",prompt="",x=513,y=63,width=150,height=219,fill="none"),
    TextSlot(id="t2",prompt="",text="4",style_role="diagram",x=344,y=74,font_size=44),TextSlot(id="t1",prompt="",text="7",style_role="diagram",x=384,y=74,font_size=44),TextSlot(id="t0",prompt="",text="3",style_role="diagram",x=424,y=74,font_size=44),
    TextSlot(id="mx",prompt="",text="?",style_role="diagram",x=300,y=114,font_size=44),TextSlot(id="m0",prompt="",text="3",style_role="diagram",x=424,y=114,font_size=44),
    LineSlot(id="l1",prompt="",x1=298,y1=122,x2=438,y2=122),
    TextSlot(id="p0",prompt="",text="9",style_role="diagram",x=424,y=156,font_size=44),
    RectSlot(id="hl",prompt="",x=368,y=168,width=88,height=38,fill="#e9c8dc"),
    TextSlot(id="h2",prompt="",text="2",style_role="diagram",x=374,y=200,font_size=44),TextSlot(id="h1",prompt="",text="1",style_role="diagram",x=408,y=200,font_size=44),TextSlot(id="h0",prompt="",text="0",style_role="diagram",x=442,y=200,font_size=44),
    TextSlot(id="p23",prompt="",text="1",style_role="diagram",x=304,y=240,font_size=44),TextSlot(id="p22",prompt="",text="2",style_role="diagram",x=344,y=240,font_size=44),TextSlot(id="p21",prompt="",text="0",style_role="diagram",x=384,y=240,font_size=44),TextSlot(id="p20",prompt="",text="0",style_role="diagram",x=424,y=240,font_size=44),
    LineSlot(id="l2",prompt="",x1=298,y1=242,x2=458,y2=242),
    TextSlot(id="f3",prompt="",text="1",style_role="diagram",x=304,y=280,font_size=44),TextSlot(id="f2",prompt="",text="4",style_role="diagram",x=344,y=280,font_size=44),TextSlot(id="f1",prompt="",text="1",style_role="diagram",x=384,y=280,font_size=44),TextSlot(id="f0",prompt="",text="9",style_role="diagram",x=424,y=280,font_size=44),
    TextSlot(id="c1",prompt="",text="7 ? 3",style_role="choice",x=536,y=112,font_size=40),TextSlot(id="c2",prompt="",text="73 ? 3",style_role="choice",x=536,y=154,font_size=40),TextSlot(id="c3",prompt="",text="70 ? 3",style_role="choice",x=536,y=196,font_size=40),TextSlot(id="c4",prompt="",text="700 ? 3",style_role="choice",x=536,y=238,font_size=40),
    TextSlot(id="a",prompt="",text="(??)73 ? 3",style_role="body",x=8,y=334,font_size=36),
    TextSlot(id="e",prompt="",text="(??)473?? 7? ?? ?? ????? 70 ? 3 = 210???.",style_role="body",x=8,y=382,font_size=40),
    ),diagrams=(),groups=(),constraints=(),tags=("??","??","??"))
PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE={"problem_id":"S3_??_3_008575","problem_type":"multiplication_place_value_choice","metadata":{"language":"ko","question":"색칠된 부분은 실제 어떤 수의 곱인지를 찾아 선택하세요.","instruction":"???? ??? ?? ????."},"domain":{"objects":[{"id":"obj.target","type":"expression","text":"73 ? 3"}],"relations":[]},"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"selected_expression","description":"??? ??? ???? ?"},"value":"73 ? 3","unit":""}}
SOLVABLE={"schema":"modu.solvable.v1.1","problem_id":"S3_??_3_008575","problem_type":"multiplication_place_value_choice","inputs":{"total_ticks":0,"target_label":"??? ??? ???? ?","target_ticks":0,"target_count":1,"unit":""},"given":[{"ref":"obj.target","value":"73 ? 3"}],"target":{"ref":"answer.target","type":"selected_expression"},"method":"place_value_matching","plan":["??? ??? ???? ????.","?? ?? ???."],"steps":[{"id":"step.1","expr":"??? ??? ?? ??","value":"73 ? 3"}],"checks":[{"id":"check.1","expr":"??","expected":"??","actual":"??","pass":True}],"answer":{"blanks":[],"choices":[],"answer_key":[],"target":{"type":"selected_expression","description":"??? ??? ???? ?"},"value":"73 ? 3","unit":""}}
