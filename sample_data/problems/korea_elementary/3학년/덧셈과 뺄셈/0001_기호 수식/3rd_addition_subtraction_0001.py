from pathlib import Path
import sys

from modu_semantic import Circle, Problem, Rect, Region, Text

CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from modu_semantic.recipes import add_curved_connector_by_anchor

CANVAS_W = 417
CANVAS_H = 220

PROBLEM_ID = "3rd_addition_subtraction_0001"
PROBLEM_TYPE = "addition_subtraction_symbol_equations"
TITLE_TEXT = "기호 수식"
INSTRUCTION_TEXT = "괄호 안에 알맞은 수의 값을 구하시오."


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


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_domain(
        {
            "instruction": INSTRUCTION_TEXT,
            "equations": ["472 + 149 = ○", "○ - △ = 285"],
            "targets": {"circle": 621, "triangle": 336},
        }
    )
    p.set_answer(
        blanks=[],
        choices=[],
        answer_key=[{"target": "answer_value", "value": "957"}],
    )

    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)
    root.add(
        Rect(
            id="bg",
            x=0,
            y=0,
            width=CANVAS_W,
            height=CANVAS_H,
            fill="#FFFFFF",
            stroke="none",
            stroke_width=0,
            semantic_role="background",
        )
    )

    lines = _wrap_text_by_width(INSTRUCTION_TEXT, font_size=17, max_width=390)
    for i, line in enumerate(lines, start=1):
        root.add(
            Text(
                id=f"instruction_{i}",
                x=6,
                y=30 + ((i - 1) * 28),
                text=line,
                font_size=17,
                font_family="Malgun Gothic",
                fill="#222222",
                anchor="start",
                semantic_role="instruction",
            )
        )

    root.add(Rect(id="left_box", x=18, y=110, width=80, height=45, fill="none", stroke="#666666", stroke_width=1.5, semantic_role="value_box"))
    root.add(Text(id="left_value", x=58, y=140, text="472", font_size=17, font_family="Malgun Gothic", fill="#222222", anchor="middle", semantic_role="label"))

    root.add(Rect(id="circle_box", x=161, y=110, width=82, height=45, fill="none", stroke="#666666", stroke_width=1.5, semantic_role="value_box"))
    root.add(Circle(id="circle_symbol", cx=202, cy=133, r=7, fill="#000000", stroke="#000000", stroke_width=1, semantic_role="symbol"))

    root.add(Rect(id="right_box", x=309, y=110, width=80, height=45, fill="none", stroke="#666666", stroke_width=1.5, semantic_role="value_box"))
    root.add(Text(id="right_value", x=349, y=140, text="285", font_size=17, font_family="Malgun Gothic", fill="#222222", anchor="middle", semantic_role="label"))

    root.add(Rect(id="plus_bubble", x=84, y=46, width=88, height=42, fill="none", stroke="#666666", stroke_width=1.4, rx=21, ry=21, semantic_role="guide"))
    root.add(Text(id="plus_text", x=128, y=73, text="+149", font_size=17, font_family="Malgun Gothic", fill="#222222", anchor="middle", semantic_role="label"))

    root.add(Rect(id="minus_bubble", x=228, y=46, width=92, height=42, fill="none", stroke="#666666", stroke_width=1.4, rx=21, ry=21, semantic_role="guide"))
    root.add(Text(id="minus_text", x=274, y=73, text="-△", font_size=17, font_family="Malgun Gothic", fill="#222222", anchor="middle", semantic_role="label"))

    boxes = {
        "left_box": (18, 110, 80, 45),
        "plus_bubble": (84, 46, 88, 42),
        "circle_box": (161, 110, 82, 45),
        "minus_bubble": (228, 46, 92, 42),
        "right_box": (309, 110, 80, 45),
    }
    add_curved_connector_by_anchor(
        root,
        aid="curve_left_to_plus",
        boxes=boxes,
        from_box="left_box",
        from_anchor="top_mid",
        to_box="plus_bubble",
        to_anchor="left_mid",
        control=(70, 84),
        arrow=False,
    )
    add_curved_connector_by_anchor(
        root,
        aid="curve_plus_to_circle",
        boxes=boxes,
        from_box="plus_bubble",
        from_anchor="right_mid",
        to_box="circle_box",
        to_anchor="top_mid",
        control=(190, 76),
        arrow=True,
    )
    add_curved_connector_by_anchor(
        root,
        aid="curve_circle_to_minus",
        boxes=boxes,
        from_box="circle_box",
        from_anchor="top_mid",
        to_box="minus_bubble",
        to_anchor="left_mid",
        control=(214, 84),
        arrow=False,
    )
    add_curved_connector_by_anchor(
        root,
        aid="curve_minus_to_right",
        boxes=boxes,
        from_box="minus_bubble",
        from_anchor="right_mid",
        to_box="right_box",
        to_anchor="top_mid",
        control=(336, 76),
        arrow=True,
    )

    root.add(Text(id="answer_left_paren", x=228, y=206, text="(", font_size=24, font_family="Malgun Gothic", fill="#222222", anchor="start", semantic_role="guide"))
    root.add(Text(id="answer_right_paren", x=394, y=206, text=")", font_size=24, font_family="Malgun Gothic", fill="#222222", anchor="start", semantic_role="guide"))
    root.add(Rect(id="answer_value", x=246, y=178, width=138, height=32, fill="none", stroke="none", stroke_width=0, semantic_role="answer_anchor"))

    p.add(root)
    return p


from _problem_runner import save_built_problem_outputs


if __name__ == "__main__":
    outputs = save_built_problem_outputs(
        build(),
        CURRENT_DIR,
        PROBLEM_ID,
        answer_overrides={"answer_overlay_numeric_font_size": 30},
    )
    print("[3rd_addition_subtraction_0001] generated:")
    print(f"  - {outputs['svg']}")
    print(f"  - {outputs['answer_svg']}")


