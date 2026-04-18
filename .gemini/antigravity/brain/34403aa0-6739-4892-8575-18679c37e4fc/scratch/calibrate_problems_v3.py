import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path("src").resolve()))

from modu_math import Problem, Text, Formula, Rect, Circle

def calibrate_0008():
    p = Problem(width=1000, height=600, problem_id="ke_3rd_0008", problem_type="sum_comparison_word_problem")
    p.title = "가전제품 소비전력 합산"
    p.set_metadata({
        "education": {"level": "elementary", "grade": 3, "subject": "math", "curriculum": "KR"},
        "classification": {"topic": "Addition and Subtraction", "sub_topic": "Word Problem", "difficulty": "medium"}
    })
    p.set_domain({
        "objects": [
            {"id": "rice_cooker", "name": "전기밥솥", "power": 500, "unit": "W"},
            {"id": "water_purifier", "name": "정수기", "power": 770, "unit": "W"},
            {"id": "monitor", "name": "모니터", "power": 150, "unit": "W"}
        ],
        "threshold": 1000,
        "combinations": [
            {"items": ["rice_cooker", "water_purifier"], "sum": 1270},
            {"items": ["rice_cooker", "monitor"], "sum": 650},
            {"items": ["water_purifier", "monitor"], "sum": 920}
        ],
        "goal": "sum_over_threshold"
    })
    p.set_answer(blanks=[{'id': 'blank_1', 'type': 'numeric'}], choices=[], answer_key=[{'blank_id': 'blank_1', 'value': 1270}])
    
    y = 60
    p.add(Text(id="t1", x=50, y=y, text="다음 가전제품 중에서 2개를 골라 소비전력의 합이 1000 W가 넘는", font_size=24, anchor="start"))
    y += 40
    p.add(Text(id="t2", x=50, y=y, text="경우를 찾아 그 합을 구하시오.", font_size=24, anchor="start"))
    
    # Items display
    items = [("전기밥솥", "500 W"), ("정수기", "770 W"), ("모니터", "150 W")]
    for i, (name, val) in enumerate(items):
        cx = 100 + i * 250
        cy = 200
        p.add(Rect(id=f"box_{i}", x=cx, y=cy, width=200, height=150, rx=10, ry=10, fill="white", stroke="black"))
        p.add(Text(id=f"name_{i}", x=cx+100, y=cy+60, text=name, font_size=28, anchor="middle"))
        p.add(Text(id=f"val_{i}", x=cx+100, y=cy+110, text=val, font_size=32, anchor="middle"))
        
    return p

def calibrate_0009():
    p = Problem(width=1000, height=600, problem_id="ke_3rd_0009", problem_type="shape_arithmetic_puzzle")
    p.title = "도형 복면산 뺄셈"
    p.set_metadata({
        "education": {"level": "elementary", "grade": 3, "subject": "math", "curriculum": "KR"},
        "classification": {"topic": "Addition and Subtraction", "sub_topic": "Vertical Arithmetic Puzzle", "difficulty": "hard"}
    })
    p.set_domain({
        "objects": [
            {"id": "square", "symbol": "■"},
            {"id": "star", "symbol": "★"}
        ],
        "vertical_subtraction": {
            "minuend": "■★■",
            "subtrahend": "★■★",
            "difference": "★73"
        },
        "values": {"square": 5, "star": 2},
        "goal": "square + star"
    })
    p.set_answer(blanks=[{'id': 'blank_1', 'type': 'numeric'}], choices=[], answer_key=[{'blank_id': 'blank_1', 'value': 7}])
    
    p.add(Text(id="t1", x=50, y=80, text="다음 뺄셈식에서 같은 모양은 같은 숫자를 나타냅니다.", font_size=24, anchor="start"))
    p.add(Text(id="t2", x=50, y=130, text="■와 ★가 나타내는 숫자의 합을 구하시오.", font_size=24, anchor="start"))
    
    # Vertical arithmetic
    base_x = 450
    p.add(Text(id="v1", x=base_x, y=250, text="  ■ ★ ■", font_size=40, anchor="start"))
    p.add(Text(id="v2", x=base_x, y=320, text="- ★ ■ ★", font_size=40, anchor="start"))
    p.add(Rect(id="line", x=base_x, y=345, width=220, height=3, fill="black"))
    p.add(Text(id="v3", x=base_x, y=410, text="  ★ 7 3", font_size=40, anchor="start"))
    
    return p

def save_all(p, num):
    path = Path(f"sample_data/problems/ke_3rd/{num}/{num}")
    p.save(path)
    print(f"Saved {num}")

save_all(calibrate_0008(), "0008")
save_all(calibrate_0009(), "0009")
