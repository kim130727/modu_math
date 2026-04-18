import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path("src").resolve()))

from modu_math import Problem, Text, Formula, Rect, Circle

def calibrate_0004():
    p = Problem(width=1000, height=500, problem_id="ke_3rd_0004", problem_type="set_word_problem")
    p.title = "국어와 수학을 모두 좋아하는 학생 수"
    p.set_answer(blanks=[{'id': 'blank_1', 'type': 'numeric'}], choices=[], answer_key=[{'blank_id': 'blank_1', 'value': 189}])
    
    y = 80
    p.add(Text(id="t1", x=50, y=y, text="국어나 수학을 좋아하는 학생 780명 중에서 국어를 좋아하는 학생이 621명,", font_size=24, anchor="start"))
    y += 40
    p.add(Text(id="t2", x=50, y=y, text="수학을 좋아하는 학생이 348명입니다. 국어와 수학을 모두 좋아하는 학생은", font_size=24, anchor="start"))
    y += 40
    p.add(Text(id="t3", x=50, y=y, text="몇 명입니까?", font_size=24, anchor="start"))
    
    return p

def calibrate_0005():
    p = Problem(width=1000, height=500, problem_id="ke_3rd_0005", problem_type="inequality_puzzle")
    p.title = "부등식을 만족하는 가장 큰 자연수"
    p.set_answer(blanks=[{'id': 'blank_1', 'type': 'numeric'}], choices=[], answer_key=[{'blank_id': 'blank_1', 'value': 488}])
    
    p.add(Text(id="t1", x=50, y=80, text="□ 안에 들어갈 수 있는 수 중에서 가장 큰 자연수를 구하시오.", font_size=24, anchor="start"))
    
    # Box around formula
    p.add(Rect(id="box", x=150, y=150, width=500, height=100, rx=10, ry=10, fill="none", stroke="#000000", stroke_width=2))
    p.add(Formula(id="f1", x=400, y=210, expr="179 + 265 < 933 - □", font_size=32, anchor="middle"))
    
    return p

def calibrate_0006():
    p = Problem(width=1000, height=600, problem_id="ke_3rd_0006", problem_type="card_number_puzzle")
    p.title = "수 카드로 만든 수의 차"
    p.set_answer(blanks=[{'id': 'blank_1', 'type': 'numeric'}], choices=[], answer_key=[{'blank_id': 'blank_1', 'value': 434}])
    
    y = 80
    p.add(Text(id="t1", x=50, y=y, text="5장의 수 카드 중에서 3장을 골라 한 번씩만 사용하여 세 자리 수를 만들었습니다.", font_size=24, anchor="start"))
    y += 40
    p.add(Text(id="t2", x=50, y=y, text="세 자리 수 중에서 십의 자리 숫자가 8인 두 번째로 큰 수와 일의 자리 숫자가", font_size=24, anchor="start"))
    y += 40
    p.add(Text(id="t3", x=50, y=y, text="8인 두 번째로 작은 수의 차는 얼마입니까?", font_size=24, anchor="start"))
    
    # Cards
    cards = ["2", "0", "4", "6", "8"]
    for i, val in enumerate(cards):
        cx = 150 + i * 100
        cy = 250
        p.add(Rect(id=f"card_box_{i}", x=cx, y=cy, width=80, height=100, rx=5, ry=5, fill="white", stroke="black"))
        p.add(Text(id=f"card_text_{i}", x=cx+40, y=cy+60, text=val, font_size=40, anchor="middle"))
        
    return p

def calibrate_0007():
    p = Problem(width=1000, height=600, problem_id="ke_3rd_0007", problem_type="expression_maximization")
    p.title = "계산 결과가 가장 큰 식 만들기"
    p.set_answer(blanks=[{'id': 'blank_1', 'type': 'numeric'}, {'id': 'blank_res', 'type': 'numeric'}], choices=[], answer_key=[{'blank_id': 'blank_res', 'value': 1372}])
    
    y = 80
    p.add(Text(id="t1", x=50, y=y, text="주어진 수 중에서 세 수를 골라 다음과 같은 식을 만들려고 합니다. 계산 결과가", font_size=24, anchor="start"))
    y += 40
    p.add(Text(id="t2", x=50, y=y, text="가장 크게 되는 식을 만들려고 할 때 □ 안에 알맞은 수를 써넣고, 계산한 값을 구하시오.", font_size=24, anchor="start"))
    
    # Given numbers in box
    p.add(Rect(id="num_box", x=150, y=180, width=500, height=80, rx=10, ry=10, fill="none", stroke="black"))
    nums = ["365", "567", "827", "910"]
    for i, n in enumerate(nums):
        p.add(Text(id=f"n{i}", x=220 + i * 120, y=230, text=n, font_size=28, anchor="middle"))
        
    # Formula structure
    p.add(Rect(id="b1", x=150, y=320, width=100, height=60, fill="none", stroke="black"))
    p.add(Text(id="op1", x=275, y=360, text="-", font_size=32, anchor="middle"))
    p.add(Rect(id="b2", x=300, y=320, width=100, height=60, fill="none", stroke="black"))
    p.add(Text(id="op2", x=425, y=360, text="+", font_size=32, anchor="middle"))
    p.add(Rect(id="b3", x=450, y=320, width=100, height=60, fill="none", stroke="black"))
    
    return p

def save_all(p, num):
    path = Path(f"sample_data/problems/ke_3rd/{num}/{num}")
    p.save(path)
    print(f"Saved {num}")

save_all(calibrate_0004(), "0004")
save_all(calibrate_0005(), "0005")
save_all(calibrate_0006(), "0006")
save_all(calibrate_0007(), "0007")
