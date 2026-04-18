from __future__ import annotations
from pathlib import Path
from modu_math import Problem, Text, Formula

PROBLEM_ID = "ke_3rd_0002"

def build() -> Problem:
    p = Problem(width=1000, height=500, problem_id=PROBLEM_ID, problem_type="equation_system_word_problem")
    p.title = "모양에 알맞은 수 구하기"
    p.set_domain({
        "objects": [
            {
                "id": "square",
                "symbol": "■"
            },
            {
                "id": "triangle",
                "symbol": "▲"
            }
        ],
        "relations": [
            {
                "id": "eq1",
                "expr": "800 - 347 + square = 650"
            },
            {
                "id": "eq2",
                "expr": "543 - triangle = square"
            }
        ],
        "values": {
            "square": 197,
            "triangle": 346
        },
        "goal": "triangle - square"
    })
    p.set_answer(blanks=[{'id': 'blank_1', 'type': 'numeric'}], choices=[], answer_key=[{'blank_id': 'blank_1', 'value': 149}])
    
    p.add(Text(id="t1", x=50.0, y=80.0, text="같은 모양은 같은 수를 나타냅니다. ■와 ▲에 알맞은 수의 차를 구하시오.", font_size=24, anchor="start"))
    p.add(Formula(id="eq1", x=80.0, y=200.0, expr="800 - 347 + ■ = 650", font_size=28, anchor="start"))
    p.add(Formula(id="eq2", x=80.0, y=300.0, expr="543 - ▲ = ■", font_size=28, anchor="start"))
    
    return p

if __name__ == "__main__":
    out_prefix = Path(__file__).resolve().parent / "0002"
    build().save(out_prefix)
