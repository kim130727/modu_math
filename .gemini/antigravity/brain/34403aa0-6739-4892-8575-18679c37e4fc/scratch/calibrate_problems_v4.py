import json
import sys
from pathlib import Path as FilePath

# Add src to path
sys.path.insert(0, str(FilePath("src").resolve()))

from modu_math import Problem, Text, Rect, Line, Path

def calibrate_0010():
    p = Problem(width=1000, height=600, problem_id="ke_3rd_0010", problem_type="length_calculation_puzzle")
    p.title = "선분의 길이 계산하기"
    p.set_metadata({
        "education": {"level": "elementary", "grade": 3, "subject": "math", "curriculum": "KR"},
        "classification": {"topic": "Length and Time", "sub_topic": "Length Calculation", "difficulty": "medium"}
    })
    p.set_domain({
        "objects": [
            {"id": "seg_left", "length": 821, "unit": "cm"},
            {"id": "seg_middle", "symbol": "㉡", "length": 212, "unit": "cm"},
            {"id": "seg_right", "length": 236, "unit": "cm"},
            {"id": "combo_left_mid", "symbol": "㉠", "formula": "seg_left + seg_middle", "value": 1033},
            {"id": "combo_mid_right", "length": 448, "formula": "seg_middle + seg_right"}
        ],
        "goal": ["㉠", "㉡"]
    })
    p.set_answer(
        blanks=[{'id': 'blank_a', 'type': 'numeric'}, {'id': 'blank_b', 'type': 'numeric'}],
        choices=[],
        answer_key=[{'blank_id': 'blank_a', 'value': 1033}, {'blank_id': 'blank_b', 'value': 212}]
    )
    
    p.add(Text(id="t1", x=50, y=80, text="㉠과 ㉡의 길이는 각각 몇 cm입니까?", font_size=24, anchor="start"))
    
    # Diagram
    base_y = 350
    x_start = 100
    w_l = 350
    w_m = 150
    w_r = 200
    
    x_l_end = x_start + w_l
    x_m_end = x_l_end + w_m
    x_r_end = x_m_end + w_r
    
    # Main horizontal line
    p.add(Line(id="main_line", x1=x_start, y1=base_y, x2=x_r_end, y2=base_y, stroke_width=3))
    
    # Ticks
    for i, x in enumerate([x_start, x_l_end, x_m_end, x_r_end]):
        p.add(Line(id=f"tick_{i}", x1=x, y1=base_y - 10, x2=x, y2=base_y + 10, stroke_width=2))
        
    # Top dashed arcs
    # L = 821
    p.add(Path(id="arc_l", d=f"M {x_start} {base_y-15} Q {(x_start+x_l_end)/2} {base_y-80} {x_l_end} {base_y-15}", 
               stroke="#000000", stroke_width=1.5, stroke_dasharray="5,5"))
    p.add(Text(id="label_l", x=x_start + w_l/2, y=base_y - 60, text="821 cm", font_size=20, anchor="middle"))
    
    # M + R = 448
    p.add(Path(id="arc_mr", d=f"M {x_l_end} {base_y-15} Q {(x_l_end+x_r_end)/2} {base_y-80} {x_r_end} {base_y-15}", 
               stroke="#000000", stroke_width=1.5, stroke_dasharray="5,5"))
    p.add(Text(id="label_mr", x=x_l_end + (w_m+w_r)/2, y=base_y - 60, text="448 cm", font_size=20, anchor="middle"))
    
    # Bottom dashed arcs
    # L + M = ㉠
    p.add(Path(id="arc_lm", d=f"M {x_start} {base_y+15} Q {(x_start+x_m_end)/2} {base_y+80} {x_m_end} {base_y+15}", 
               stroke="#000000", stroke_width=1.5, stroke_dasharray="5,5"))
    p.add(Text(id="label_lm", x=x_start + (w_l+w_m)/2, y=base_y + 70, text="㉠", font_size=20, anchor="middle"))
    
    # M = ㉡
    p.add(Path(id="arc_m", d=f"M {x_l_end} {base_y+15} Q {(x_l_end+x_m_end)/2} {base_y+120} {x_m_end} {base_y+15}", 
               stroke="#000000", stroke_width=1.5, stroke_dasharray="5,5"))
    p.add(Text(id="label_m", x=x_l_end + w_m/2, y=base_y + 110, text="㉡", font_size=20, anchor="middle"))
    
    # R = 236
    p.add(Path(id="arc_r", d=f"M {x_m_end} {base_y+15} Q {(x_m_end+x_r_end)/2} {base_y+80} {x_r_end} {base_y+15}", 
               stroke="#000000", stroke_width=1.5, stroke_dasharray="5,5"))
    p.add(Text(id="label_r", x=x_m_end + w_r/2, y=base_y + 70, text="236 cm", font_size=20, anchor="middle"))
    
    return p

def save_all(p, num):
    path = FilePath(f"sample_data/problems/ke_3rd/{num}/{num}")
    p.save(path)
    print(f"Saved {num}")

save_all(calibrate_0010(), "0010")
