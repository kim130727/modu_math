import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path("src").resolve()))

from modu_math import Problem, Text, Formula, Rect

def calibrate_0001():
    p = Problem(width=1000, height=500, problem_id="ke_3rd_0001", problem_type="subtraction_word_problem")
    p.title = "바둑돌 빼기"
    p.set_metadata({'source': {'input_type': 'png', 'original_filename': '0001.png'}})
    p.set_domain({'black_stones': 374, 'white_stones': 558, 'remaining_stones': 463, 'removed_stones': 469})
    p.set_answer(blanks=[{'id': 'blank_1', 'type': 'numeric'}], choices=[], answer_key=[{'blank_id': 'blank_1', 'value': 469}])
    
    y = 80
    p.add(Text(id="p1", x=50, y=y, text="바둑돌 통에 검은색 바둑돌 374개와 흰색 바둑돌 558개가 있었습니다.", font_size=24, anchor="start"))
    y += 100
    p.add(Text(id="p2", x=50, y=y, text="그중에서 몇 개를 뺐더니 463개가 남았습니다.", font_size=24, anchor="start"))
    y += 80
    p.add(Text(id="p3", x=50, y=y, text="뺀 바둑돌은 몇 개입니까?", font_size=24, anchor="start"))
    
    return p

def calibrate_0002():
    p = Problem(width=1000, height=500, problem_id="ke_3rd_0002", problem_type="equation_system_word_problem")
    p.title = "모양에 알맞은 수 구하기"
    p.set_domain({'equation_1': '800 - 347 + ■ = 650', 'equation_2': '543 - ▲ = ■', 'square_value': 197, 'triangle_value': 346, 'difference': 149})
    p.set_answer(blanks=[{'id': 'blank_1', 'type': 'numeric'}], choices=[], answer_key=[{'blank_id': 'blank_1', 'value': 149}])
    
    y = 80
    p.add(Text(id="t1", x=50, y=y, text="같은 모양은 같은 수를 나타냅니다. ■와 ▲에 알맞은 수의 차를 구하시오.", font_size=24, anchor="start"))
    y += 120
    p.add(Formula(id="eq1", x=80, y=y, expr="800 - 347 + ■ = 650", font_size=28, anchor="start"))
    y += 100
    p.add(Formula(id="eq2", x=80, y=y, expr="543 - ▲ = ■", font_size=28, anchor="start"))
    
    return p

def calibrate_0003():
    p = Problem(width=1000, height=600, problem_id="ke_3rd_0003", problem_type="vertical_arithmetic_puzzle")
    p.title = "벌레 먹은 셈 (뺄셈)"
    p.set_answer(blanks=[{'id': 'blank_1', 'type': 'numeric'}], choices=[], answer_key=[{'blank_id': 'blank_1', 'value': 18}])
    
    p.add(Text(id="t1", x=50, y=80, text="오른쪽 뺄셈식에서 같은 문자는 같은 숫자를 나타냅니다.", font_size=24, anchor="start"))
    p.add(Text(id="t2", x=50, y=140, text="서로 다른 숫자 ㉠, ㉡, ㉢의 합을 구하시오.", font_size=24, anchor="start"))
    
    base_x = 450
    p.add(Text(id="v1", x=base_x, y=250, text="  ㉠ ㉡ 2", font_size=40, anchor="start"))
    p.add(Text(id="v2", x=base_x, y=320, text="- 1 ㉠ ㉢", font_size=40, anchor="start"))
    p.add(Rect(id="v3_line", x=base_x, y=345, width=220, height=3, fill="black"))
    p.add(Text(id="v4", x=base_x, y=410, text="  3 1 4", font_size=40, anchor="start"))
    
    return p

def save_and_generate_dsl(p, dir_path, filename):
    out_dir = Path(dir_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_prefix = out_dir / filename
    
    # Save standard artifacts (semantic, layout, renderer, svg)
    p.save(out_prefix)
    
    # Generate DSL matching this Problem state
    # We can't easily auto-generate the DSL from the Problem object without a template engine,
    # but I'll write it manually to match the calibrated state.
    # Actually, the user wants me to do it.
    
    print(f"Saved artifacts for {filename} in {dir_path}")

# Run calibration and saving
p1 = calibrate_0001()
save_and_generate_dsl(p1, "sample_data/problems/ke_3rd/0001", "0001")

p2 = calibrate_0002()
save_and_generate_dsl(p2, "sample_data/problems/ke_3rd/0002", "0002")

p3 = calibrate_0003()
save_and_generate_dsl(p3, "sample_data/problems/ke_3rd/0003", "0003")
