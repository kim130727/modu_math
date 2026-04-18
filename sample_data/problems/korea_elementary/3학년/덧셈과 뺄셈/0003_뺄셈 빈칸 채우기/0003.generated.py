from __future__ import annotations
from pathlib import Path
from modu_math import Problem, Text, Rect

PROBLEM_ID = "ke_3rd_0003"

def build() -> Problem:
    p = Problem(width=1000, height=600, problem_id=PROBLEM_ID, problem_type="vertical_arithmetic_puzzle")
    p.title = "벌레 먹은 셈 (뺄셈)"
    p.set_answer(blanks=[{'id': 'blank_1', 'type': 'numeric'}], choices=[], answer_key=[{'blank_id': 'blank_1', 'value': 18}])
    
    p.add(Text(id="t1", x=50.0, y=80.0, text="오른쪽 뺄셈식에서 같은 문자는 같은 숫자를 나타냅니다.", font_size=24, anchor="start"))
    p.add(Text(id="t2", x=50.0, y=140.0, text="서로 다른 숫자 ㉠, ㉡, ㉢의 합을 구하시오.", font_size=24, anchor="start"))
    
    base_x = 450.0
    p.add(Text(id="v1", x=base_x, y=250.0, text="  ㉠ ㉡ 2", font_size=40, anchor="start"))
    p.add(Text(id="v2", x=base_x, y=320.0, text="- 1 ㉠ ㉢", font_size=40, anchor="start"))
    p.add(Rect(id="v3_line", x=base_x, y=345.0, width=220.0, height=3.0, fill="black"))
    p.add(Text(id="v4", x=base_x, y=410.0, text="  3 1 4", font_size=40, anchor="start"))
    
    return p

if __name__ == "__main__":
    out_prefix = Path(__file__).resolve().parent / "0003"
    build().save(out_prefix)
