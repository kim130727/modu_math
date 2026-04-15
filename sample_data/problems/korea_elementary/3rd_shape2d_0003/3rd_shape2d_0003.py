from pathlib import Path
import sys

from modu_semantic import Line, Problem, Rect, Region, Text

CANVAS_W = 440
CANVAS_H = 361

PROBLEM_ID = "3rd_shape2d_0003"
PROBLEM_TYPE = "shape2d_find_all_names"
TITLE_TEXT = "도형 이름 고르기"
INSTRUCTION_TEXT = "도형의 이름으로 알맞은 것을 모두 찾아 기호를 쓰시오."

ANSWER_LABEL = "㉡㉣"


def _wrap_text_by_width(text: str, *, font_size: float, max_width: float) -> list[str]:
    if not text:
        return [""]
    approx_char_w = font_size * 0.92
    max_chars = max(1, int(max_width / approx_char_w))
    words = text.split(" ")
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                lines.append(current)
                current = word
            else:
                for i in range(0, len(word), max_chars):
                    chunk = word[i : i + max_chars]
                    if len(chunk) == max_chars:
                        lines.append(chunk)
                    else:
                        current = chunk
    if current:
        lines.append(current)
    return lines or [text]


def _add_instruction(root: Region) -> None:
    lines = _wrap_text_by_width(INSTRUCTION_TEXT, font_size=17, max_width=398)
    for i, line in enumerate(lines, start=1):
        root.add(
            Text(
                id=f"instruction_{i}",
                x=4,
                y=33 + ((i - 1) * 32),
                text=line,
                font_size=17,
                font_family="Malgun Gothic",
                fill="#222222",
                anchor="start",
                semantic_role="instruction",
            )
        )


def _add_grid(root: Region) -> None:
    x0 = 149
    y0 = 78
    step = 22
    cols = 6
    rows = 6
    stroke = "#767676"

    root.add(
        Rect(
            id="grid_box",
            x=x0,
            y=y0,
            width=step * (cols - 1),
            height=step * (rows - 1),
            fill="none",
            stroke=stroke,
            stroke_width=1.2,
            semantic_role="guide",
            metadata={"stroke_dasharray": "4 4"},
        )
    )
    for i in range(cols):
        x = x0 + (i * step)
        root.add(
            Line(
                id=f"grid_v_{i}",
                x1=x,
                y1=y0,
                x2=x,
                y2=y0 + (step * (rows - 1)),
                stroke=stroke,
                stroke_width=1.2,
                semantic_role="guide",
                metadata={"stroke_dasharray": "4 4"},
            )
        )
    for j in range(rows):
        y = y0 + (j * step)
        root.add(
            Line(
                id=f"grid_h_{j}",
                x1=x0,
                y1=y,
                x2=x0 + (step * (cols - 1)),
                y2=y,
                stroke=stroke,
                stroke_width=1.2,
                semantic_role="guide",
                metadata={"stroke_dasharray": "4 4"},
            )
        )

    root.add(
        Rect(
            id="target_shape",
            x=171,
            y=100,
            width=66,
            height=66,
            fill="none",
            stroke="#2D2D2D",
            stroke_width=3,
            semantic_role="shape",
        )
    )


def _add_choice(root: Region, *, key: str, text: str, x: float, y: float) -> None:
    root.add(
        Text(
            id=f"choice_key_{key}",
            x=x,
            y=y,
            text=f"{key} {text}",
            font_size=17,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="choice",
        )
    )


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_domain(
        {
            "instruction": INSTRUCTION_TEXT,
            "shape_name_choices": {
                "㉠": "직사각형",
                "㉡": "사각형",
                "㉢": "직각삼각형",
                "㉣": "정사각형",
            },
            "correct_labels": ["㉡", "㉣"],
        }
    )
    p.set_answer(
        blanks=[],
        choices=[],
        answer_key=[
            {"target": "answer_blank", "value": ANSWER_LABEL},
        ],
    )

    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    root.add(
        Rect(
            id="bg",
            x=0,
            y=0,
            width=CANVAS_W,
            height=CANVAS_H,
            fill="#F4F4F4",
            stroke="none",
            stroke_width=0,
            semantic_role="background",
        )
    )
    _add_instruction(root)
    _add_grid(root)

    root.add(
        Rect(
            id="choice_box",
            x=4,
            y=213,
            width=399,
            height=88,
            fill="none",
            stroke="#6D6D6D",
            stroke_width=1.8,
            rx=12,
            ry=12,
            semantic_role="guide",
        )
    )
    _add_choice(root, key="㉠", text="직사각형", x=20, y=248)
    _add_choice(root, key="㉡", text="사각형", x=206, y=248)
    _add_choice(root, key="㉢", text="직각삼각형", x=20, y=280)
    _add_choice(root, key="㉣", text="정사각형", x=206, y=280)

    root.add(
        Text(
            id="answer_left_paren",
            x=170,
            y=345,
            text="(",
            font_size=44,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="guide",
        )
    )
    root.add(
        Text(
            id="answer_right_paren",
            x=394,
            y=345,
            text=")",
            font_size=44,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="guide",
        )
    )
    root.add(
        Rect(
            id="answer_blank",
            x=188,
            y=318,
            width=188,
            height=34,
            fill="none",
            stroke="none",
            stroke_width=0,
            semantic_role="answer_anchor",
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
        PROBLEM_ID,
        answer_overrides={"answer_overlay_font_size": 34},
    )
    print("[3rd_shape2d_0003] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")
