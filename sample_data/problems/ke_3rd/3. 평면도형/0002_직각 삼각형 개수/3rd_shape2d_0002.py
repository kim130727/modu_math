from pathlib import Path
import sys

from modu_semantic import Circle, Line, Problem, Rect, Region, Text

CANVAS_W = 768
CANVAS_H = 667

PROBLEM_ID = "3rd_shape2d_0002"
PROBLEM_TYPE = "shape2d_right_triangle_with_segment"
TITLE_TEXT = "선분으로 직각삼각형 만들기"
INSTRUCTION_TEXT = "선분 ㄱㄴ을 변으로 하는 직각삼각형을 그리고 싶습니다. 이을 점을 찾아 선을 긋고, 직각삼각형을 완성해 보세요."

INSTR_X = 24
INSTR_Y = 58
INSTR_FONT = 34
INSTR_LINE_H = 42
INSTR_MAX_X = CANVAS_W - 36

GRID_X = 58
GRID_Y = 180
GRID_W = 640
GRID_H = 320
GRID_STEP = 40

BASE_START = (257, 459)
BASE_END = (579, 459)
CHOICES = [
    ("ㄷ", (178, 300)),
    ("ㄹ", (298, 259)),
    ("ㅁ", (377, 259)),
    ("ㅂ", (579, 259)),
    ("ㅅ", (619, 339)),
]
ANSWER_POINT_LABEL = "ㅂ"


def _wrap_text_by_width(text: str, *, font_size: float, max_width: float) -> list[str]:
    if not text:
        return [""]
    # 한글 문장 기준으로 보수적으로 폭을 계산해 우측 침범을 줄인다.
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


def _add_grid(root: Region) -> None:
    root.add(
        Rect(
            id="grid_box",
            x=GRID_X,
            y=GRID_Y,
            width=GRID_W,
            height=GRID_H,
            stroke="#9CA3AF",
            stroke_width=2,
            fill="none",
            semantic_role="guide",
            metadata={"stroke_dasharray": "6 6"},
        )
    )
    for i in range(17):
        x = GRID_X + (i * GRID_STEP)
        root.add(
            Line(
                id=f"grid_v_{i:02d}",
                x1=x,
                y1=GRID_Y,
                x2=x,
                y2=GRID_Y + GRID_H,
                stroke="#9CA3AF",
                stroke_width=1,
                semantic_role="guide",
                metadata={"stroke_dasharray": "5 7"},
            )
        )
    for j in range(9):
        y = GRID_Y + (j * GRID_STEP)
        root.add(
            Line(
                id=f"grid_h_{j:02d}",
                x1=GRID_X,
                y1=y,
                x2=GRID_X + GRID_W,
                y2=y,
                stroke="#9CA3AF",
                stroke_width=1,
                semantic_role="guide",
                metadata={"stroke_dasharray": "5 7"},
            )
        )


def _add_point_with_label(root: Region, *, pid: str, label_id: str, label_text: str, x: float, y: float) -> None:
    root.add(
        Circle(
            id=pid,
            cx=x,
            cy=y,
            r=5,
            fill="#222222",
            stroke="none",
            stroke_width=0,
            semantic_role="point",
        )
    )
    root.add(
        Text(
            id=label_id,
            x=x + 8,
            y=y - 8,
            text=label_text,
            font_size=34,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="label",
        )
    )


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id=PROBLEM_ID, problem_type=PROBLEM_TYPE)
    p.title = TITLE_TEXT
    p.set_domain(
        {
            "base_segment": {"start_label": "ㄱ", "end_label": "ㄴ"},
            "choice_points": [item[0] for item in CHOICES],
            "answer_point": ANSWER_POINT_LABEL,
            "instruction": INSTRUCTION_TEXT,
        }
    )
    p.set_answer(
        blanks=[],
        choices=[],
        answer_key=[{"target": "answer_point", "value": ANSWER_POINT_LABEL}],
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
    _add_grid(root)
    _add_point_with_label(
        root, pid="dot_base_start", label_id="label_base_start", label_text="ㄱ", x=BASE_START[0], y=BASE_START[1]
    )
    _add_point_with_label(
        root, pid="dot_base_end", label_id="label_base_end", label_text="ㄴ", x=BASE_END[0], y=BASE_END[1]
    )
    for idx, (label, (x, y)) in enumerate(CHOICES, start=1):
        _add_point_with_label(
            root,
            pid=f"dot_choice_{idx}",
            label_id=f"label_choice_{idx}",
            label_text=label,
            x=x,
            y=y,
        )
    root.add(
        Line(
            id="base_segment",
            x1=BASE_START[0],
            y1=BASE_START[1],
            x2=BASE_END[0],
            y2=BASE_END[1],
            stroke="#222222",
            stroke_width=4,
            semantic_role="given_segment",
        )
    )
    root.add(
        Rect(
            id="answer_point",
            x=640,
            y=611,
            width=60,
            height=42,
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
    outputs = save_built_problem_outputs(build(), CURRENT_DIR, PROBLEM_ID)
    print("[3rd_shape2d_0002] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")
