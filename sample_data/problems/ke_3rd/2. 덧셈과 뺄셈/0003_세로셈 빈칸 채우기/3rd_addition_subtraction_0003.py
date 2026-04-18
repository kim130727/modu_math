from pathlib import Path
import sys

from modu_semantic import Problem, Rect, Region, Text

CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from modu_semantic.recipes import add_masked_number_pattern

CANVAS_W = 311
CANVAS_H = 192

PROBLEM_ID = "3rd_addition_subtraction_0003"
PROBLEM_TYPE = "vertical_addition_fill_blanks"
INSTRUCTION_TEXT = "□ 안에 알맞은 수를 써넣으세요."


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = "세로셈 빈칸 채우기"
    p.set_domain(
        {
            "instruction": INSTRUCTION_TEXT,
            "equation": "□26 + 5□□ = 1304",
            "resolved": "726 + 578 = 1304",
        }
    )
    p.set_answer(
        blanks=[],
        choices=[],
        answer_key=[
            {"target": "blank_top", "value": "7"},
            {"target": "blank_mid", "value": "7"},
            {"target": "blank_low", "value": "8"},
        ],
    )

    r = Region(id="root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    r.add(Rect(id="bg", x=0, y=0, width=CANVAS_W, height=CANVAS_H, fill="#FFFFFF", stroke="none", stroke_width=0))
    r.add(Text(id="t1", x=6, y=30, text=INSTRUCTION_TEXT, font_size=17, font_family="Malgun Gothic", fill="#222222"))

    col_thousands = 145
    col_hundreds = 184
    col_tens = 225
    col_ones = 265
    digit_columns = [col_thousands, col_hundreds, col_tens, col_ones]
    digit_font = 17

    add_masked_number_pattern(
        r,
        aid="top",
        pattern="□26",
        columns=digit_columns,
        y=72,
        blank_ids=["blank_top"],
        font_size=digit_font,
    )

    r.add(Text(id="plus", x=140, y=116, text="+", font_size=34, font_family="Malgun Gothic", fill="#222222"))
    add_masked_number_pattern(
        r,
        aid="mid",
        pattern="5□□",
        columns=digit_columns,
        y=115,
        blank_ids=["blank_mid", "blank_low"],
        font_size=digit_font,
    )

    r.add(Rect(id="sep", x=112, y=144, width=182, height=1, fill="#777777", stroke="none", stroke_width=0))
    add_masked_number_pattern(
        r,
        aid="ans",
        pattern="1304",
        columns=digit_columns,
        y=174,
        font_size=digit_font,
    )

    p.add(r)
    return p


from _problem_runner import save_built_problem_outputs

if __name__ == "__main__":
    outputs = save_built_problem_outputs(build(), CURRENT_DIR, PROBLEM_ID, answer_overrides={"answer_overlay_numeric_font_size": 17})
    print("[3rd_addition_subtraction_0003] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")


