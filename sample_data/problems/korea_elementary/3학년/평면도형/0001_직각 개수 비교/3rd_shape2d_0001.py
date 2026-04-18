from pathlib import Path
import sys

from modu_semantic import Circle, Problem, Rect, Region, Text
from modu_semantic.recipes import add_polygon_with_vertices, quarter_sector_points

CANVAS_W = 411
CANVAS_H = 279

PROBLEM_ID = "3rd_shape2d_0001"
PROBLEM_TYPE = "shape2d_count_right_angles"
TITLE_TEXT = "직각의 개수 비교"
INSTRUCTION_TEXT = "직각이 가장 많은 도형과 가장 적은 도형을 찾아 차례로 기호를 쓰세요."

INSTR_X = 10
INSTR_Y = 33
INSTR_FONT = 17
INSTR_LINE_H = 32
INSTR_MAX_X = CANVAS_W - 10

FRAME_X = 10
FRAME_Y = 74
FRAME_W = 391
FRAME_H = 194

ANSWER_MOST_LABEL = "ㄱ"
ANSWER_LEAST_LABEL = "ㄴ"


def _wrap_text_by_width(text: str, *, font_size: float, max_width: float) -> list[str]:
    if not text:
        return [""]
    approx_char_w = font_size * 0.95
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


def _add_instruction_text(root: Region) -> None:
    lines = _wrap_text_by_width(
        INSTRUCTION_TEXT,
        font_size=INSTR_FONT,
        max_width=INSTR_MAX_X - INSTR_X,
    )
    for i, line in enumerate(lines, start=1):
        root.add(
            Text(
                id=f"instruction_{i}",
                x=INSTR_X,
                y=INSTR_Y + (i - 1) * INSTR_LINE_H,
                text=line,
                font_size=INSTR_FONT,
                font_family="Malgun Gothic",
                fill="#222222",
                anchor="start",
                semantic_role="instruction",
            )
        )


def _add_choice_label(root: Region, *, label: str, cx: float, cy: float) -> None:
    root.add(
        Circle(
            id=f"label_circle_{label}",
            cx=cx,
            cy=cy,
            r=8,
            fill="none",
            stroke="#666666",
            stroke_width=1.6,
            semantic_role="label_marker",
        )
    )
    root.add(
        Text(
            id=f"label_text_{label}",
            x=cx,
            y=cy + 5,
            text=label,
            font_size=14,
            font_family="Malgun Gothic",
            fill="#555555",
            anchor="middle",
            semantic_role="label",
        )
    )


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_domain(
        {
            "instruction": INSTRUCTION_TEXT,
            "shape_labels": ["ㄱ", "ㄴ", "ㄷ", "ㄹ"],
            "most_right_angles": ANSWER_MOST_LABEL,
            "least_right_angles": ANSWER_LEAST_LABEL,
        }
    )
    p.set_answer(
        blanks=[],
        choices=[],
        answer_key=[
            {"target": "answer_most", "value": ANSWER_MOST_LABEL},
            {"target": "answer_least", "value": ANSWER_LEAST_LABEL},
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
    _add_instruction_text(root)

    root.add(
        Rect(
            id="problem_frame",
            x=FRAME_X,
            y=FRAME_Y,
            width=FRAME_W,
            height=FRAME_H,
            fill="none",
            stroke="#7A7A7A",
            stroke_width=1.3,
            rx=10,
            ry=10,
            semantic_role="guide",
        )
    )

    _add_choice_label(root, label="ㄱ", cx=35, cy=101)
    _add_choice_label(root, label="ㄴ", cx=214, cy=100)
    _add_choice_label(root, label="ㄷ", cx=35, cy=199)
    _add_choice_label(root, label="ㄹ", cx=214, cy=199)

    add_polygon_with_vertices(
        root,
        shape_id="shape_giyeok",
        points=[(92, 92), (133, 133), (92, 174), (51, 133)],
        vertex_ids=["A", "B", "C", "D"],
    )
    add_polygon_with_vertices(
        root,
        shape_id="shape_nieun",
        points=quarter_sector_points(cx=230, cy=169, r=79, steps=24),
        vertex_ids=[f"Q{i}" for i in range(27)],
    )
    add_polygon_with_vertices(
        root,
        shape_id="shape_digeut",
        points=[(52, 251), (88, 191), (148, 191), (149, 250)],
        vertex_ids=["E", "F", "G", "H"],
    )
    add_polygon_with_vertices(
        root,
        shape_id="shape_rieul",
        points=[(232, 251), (232, 214), (274, 191), (318, 191), (318, 251)],
        vertex_ids=["I", "J", "K", "L", "M"],
    )

    root.add(
        Rect(
            id="answer_most",
            x=342,
            y=16,
            width=24,
            height=24,
            fill="none",
            stroke="none",
            stroke_width=0,
            semantic_role="answer_anchor",
        )
    )
    root.add(
        Rect(
            id="answer_least",
            x=374,
            y=16,
            width=24,
            height=24,
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
    print("[3rd_shape2d_0001] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")
