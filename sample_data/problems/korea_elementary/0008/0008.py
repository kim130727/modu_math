"""문제 0008 DSL 빌드 파일. 덧셈 빈칸과 숫자-글자 매핑 박스를 함께 구성합니다."""

from pathlib import Path
import sys

from modu_semantic import Line, Problem, Rect, Region, Text

# 레이아웃 상수
CANVAS_W = 981
CANVAS_H = 818

INSTRUCTION_1 = "□안에 알맞은 수를 넣고 그 수를 이용하여"
INSTRUCTION_2 = "숨어 있는 글자를 찾아 보세요."

INSTRUCTION_X = 50.109848
INSTRUCTION_Y1 = 80.148636
INSTRUCTION_Y2 = 146.62199

BOARD_X = 176.71027
BOARD_Y = 238.9496
BOARD_W = 634.32971
BOARD_H = 475.86401

EQ1_X = 426.39066
EQ2_X = 699.39069
EQ_TOP_Y = 327.78397
EQ_MID_Y = 403.78397
EQ_LINE_Y = 446.78397

HINT_BOX_X = 215.84605
HINT_BOX_Y = 521.72571
HINT_BOX_W = 560
HINT_BOX_H = 148
HINT_TEXT_X = HINT_BOX_X + (HINT_BOX_W / 2)
HINT_TEXT_Y = HINT_BOX_Y + 58
HINT_TEXT_MAX_CHARS = 26
HINT_LINE_HEIGHT = 42

BLANK_W = 46
BLANK_H = 46
BLANK_Y = 454.78397
BLANK_STEP = 54

EQ1_BLANK_X0 = 276.39066
EQ2_BLANK_X0 = 550.39069

DIGIT_TOKENS = [
    "1=나",
    "2=이",
    "3=요",
    "4=구",
    "5=꿍",
    "6=월",
    "7=친",
    "8=와",
    "9=짝",
    "0=너",
]


def _wrap_tokens(tokens: list[str], *, max_chars: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for token in tokens:
        candidate = token if not current else f"{current}  {token}"
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            lines.append(current)
        current = token
    if current:
        lines.append(current)
    return lines


def _add_digit_hint_lines(root: Region) -> None:
    lines = _wrap_tokens(DIGIT_TOKENS, max_chars=HINT_TEXT_MAX_CHARS)
    for i, line in enumerate(lines):
        root.add(
            Text(
                id=f"map_line_{i + 1}",
                x=HINT_TEXT_X,
                y=HINT_TEXT_Y + (HINT_LINE_HEIGHT * i),
                text=line,
                font_size=30,
                font_family="Malgun Gothic",
                anchor="middle",
                fill="#333333",
                semantic_role="hint_text",
            )
        )


# 레이아웃 상수
def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id="0008", problem_type="addition_code_word")
    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)

    root.add(
        Text(
            id="inst",
            x=INSTRUCTION_X,
            y=INSTRUCTION_Y1,
            text=INSTRUCTION_1,
            font_size=45,
            font_family="Malgun Gothic",
            anchor="start",
            fill="#222222",
            semantic_role="instruction",
        )
    )
    root.add(
        Text(
            id="inst_2",
            x=46.293472,
            y=INSTRUCTION_Y2,
            text=INSTRUCTION_2,
            font_size=44,
            font_family="Malgun Gothic",
            anchor="start",
            fill="#222222",
            semantic_role="instruction",
        )
    )

    root.add(
        Rect(
            id="board",
            x=BOARD_X,
            y=BOARD_Y,
            width=BOARD_W,
            height=BOARD_H,
            rx=32.739597,
            stroke="#B58D61",
            stroke_width=8.29893,
            fill="#EFDDBB",
            semantic_role="container",
        )
    )

    root.add(
        Text(
            id="eq1_top",
            x=EQ1_X,
            y=EQ_TOP_Y,
            text="127",
            font_size=62,
            font_family="Cambria",
            anchor="end",
            fill="#222222",
            semantic_role="equation_operand",
        )
    )
    root.add(
        Text(
            id="eq1_mid",
            x=EQ1_X,
            y=EQ_MID_Y,
            text="+621",
            font_size=62,
            font_family="Cambria",
            anchor="end",
            fill="#222222",
            semantic_role="equation_operand",
        )
    )
    root.add(
        Line(
            id="eq1_line",
            x1=224.39067,
            y1=EQ_LINE_Y,
            x2=439.39066,
            y2=EQ_LINE_Y,
            stroke="#333333",
            stroke_width=2,
            semantic_role="equation_bar",
        )
    )

    root.add(
        Text(
            id="eq2_top",
            x=EQ2_X,
            y=EQ_TOP_Y,
            text="231",
            font_size=62,
            font_family="Cambria",
            anchor="end",
            fill="#222222",
            semantic_role="equation_operand",
        )
    )
    root.add(
        Text(
            id="eq2_mid",
            x=EQ2_X,
            y=EQ_MID_Y,
            text="+764",
            font_size=62,
            font_family="Cambria",
            anchor="end",
            fill="#222222",
            semantic_role="equation_operand",
        )
    )
    root.add(
        Line(
            id="eq2_line",
            x1=497.39066,
            y1=EQ_LINE_Y,
            x2=712.39069,
            y2=EQ_LINE_Y,
            stroke="#333333",
            stroke_width=2,
            semantic_role="equation_bar",
        )
    )

    root.add(
        Rect(
            id="map_box",
            x=HINT_BOX_X,
            y=HINT_BOX_Y,
            width=HINT_BOX_W,
            height=HINT_BOX_H,
            rx=34,
            stroke="#000000",
            stroke_width=0,
            fill="#F9F9F9",
            semantic_role="hint_box",
        )
    )
    _add_digit_hint_lines(root)

    for i in range(3):
        root.add(
            Rect(
                id=f"eq1_blank_{i}",
                x=EQ1_BLANK_X0 + (BLANK_STEP * i),
                y=BLANK_Y,
                width=BLANK_W,
                height=BLANK_H,
                rx=6,
                stroke="#69BEEA",
                stroke_width=3,
                fill="none",
                semantic_role="answer_blank",
            )
        )
        root.add(
            Rect(
                id=f"eq2_blank_{i}",
                x=EQ2_BLANK_X0 + (BLANK_STEP * i),
                y=BLANK_Y,
                width=BLANK_W,
                height=BLANK_H,
                rx=6,
                stroke="#69BEEA",
                stroke_width=3,
                fill="none",
                semantic_role="answer_blank",
            )
        )

    p.add(root)
    return p


CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from _problem_runner import save_built_problem_outputs


if __name__ == "__main__":
    outputs = save_built_problem_outputs(
        build(),
        CURRENT_DIR,
        "0008",
        answer_semantic_path=CURRENT_DIR / "input" / "json" / "semantic_final.json",
    )
    print("[0008] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")
