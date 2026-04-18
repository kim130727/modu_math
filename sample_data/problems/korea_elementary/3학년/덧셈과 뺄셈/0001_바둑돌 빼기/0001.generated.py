from __future__ import annotations
from pathlib import Path
from modu_math import Problem, Text

PROBLEM_ID = "ke_3rd_0001"

def build() -> Problem:
    p = Problem(width=1000, height=500, problem_id=PROBLEM_ID, problem_type="subtraction_word_problem")
    p.title = "바둑돌 빼기"
    p.set_metadata({
        "source": {
            "input_type": "png",
            "original_filename": "0001.png"
        },
        "education": {
            "level": "elementary",
            "grade": 3,
            "subject": "math",
            "curriculum": "KR"
        },
        "classification": {
            "topic": "Addition and Subtraction",
            "sub_topic": "Word Problem",
            "difficulty": "easy"
        }
    })
    p.set_domain({
        "objects": [
            {
                "id": "black_stones",
                "count": 374,
                "unit": "개"
            },
            {
                "id": "white_stones",
                "count": 558,
                "unit": "개"
            },
            {
                "id": "total_stones",
                "formula": "black_stones + white_stones",
                "value": 932
            },
            {
                "id": "remaining_stones",
                "count": 463,
                "unit": "개"
            },
            {
                "id": "removed_stones",
                "formula": "total_stones - remaining_stones",
                "value": 469
            }
        ],
        "goal": "removed_stones"
    })
    p.set_answer(blanks=[{'id': 'blank_1', 'type': 'numeric'}], choices=[], answer_key=[{'blank_id': 'blank_1', 'value': 469}])
    
    p.add(Text(id="p1", x=50.0, y=80.0, text="바둑돌 통에 검은색 바둑돌 374개와 흰색 바둑돌 558개가 있었습니다.", font_size=24, anchor="start"))
    p.add(Text(id="p2", x=50.0, y=180.0, text="그중에서 몇 개를 뺐더니 463개가 남았습니다.", font_size=24, anchor="start"))
    p.add(Text(id="p3", x=50.0, y=260.0, text="뺀 바둑돌은 몇 개입니까?", font_size=24, anchor="start"))
    
    return p

if __name__ == "__main__":
    out_prefix = Path(__file__).resolve().parent / "0001"
    build().save(out_prefix)
