import sys
from pathlib import Path

def find_project_root(start_path: Path) -> Path:
    curr = start_path.resolve()
    while curr.parent != curr:
        if (curr / "src").exists():
            return curr
        curr = curr.parent
    return start_path.resolve()

PROJECT_ROOT = find_project_root(Path(__file__).resolve().parent)
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))
if str(PROJECT_ROOT / "sample_data" / "problems") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "sample_data" / "problems"))

from modu_semantic import Line, Problem, Rect, Region, Text, Path

ANSWER_LABEL_STYLE = {
    "use_answer_label": True,
    "answer_label_x": 980,
    "answer_label_y": 520,
    "answer_label_font_size": 44,
    "answer_label_anchor": "start",
    "answer_label_baseline": "hanging",
    "answer_label_prefix": "Answer: ",
}

# 레이아웃 상수
CANVAS_W = 1280
CANVAS_H = 720

INSTRUCTION_X = 42
INSTRUCTION_Y = 72

MODEL_BOX_X = 170
MODEL_BOX_Y = 178
MODEL_BOX_W = 615
MODEL_BOX_H = 482
MODEL_DIVIDER_Y = 402

EQUATION_X = 980
EQUATION_Y = 615
ANSWER_BLANK_X = 1120
ANSWER_BLANK_Y = 576
ANSWER_BLANK_W = 135
ANSWER_BLANK_H = 78

TOP_ROW = {
    "hundreds": 2,
    "tens": 3,
    "ones": 5,
    "hundred_base_x": 200,
    "hundred_base_y": 200,
    "ten_base_x": 420,
    "ten_base_y": 254,
    "one_base_x": 615,
    "one_base_y": 278,
}

BOTTOM_ROW = {
    "hundreds": 3,
    "tens": 5,
    "ones": 4,
    "hundred_base_x": 200,
    "hundred_base_y": 428,
    "ten_base_x": 420,
    "ten_base_y": 475,
    "one_base_x": 615,
    "one_base_y": 523,
}


def _add_hundred_block(root: Region, *, block_id: str, x: float, y: float) -> None:
    root.add(
        Rect(
            id=block_id,
            x=x,
            y=y,
            width=140,
            height=140,
            fill="#F2CF43",
            stroke="#D3AE1D",
            stroke_width=2,
            semantic_role="hundred_block",
        )
    )
    # Draw grid as a single path to keep JSON concise
    v_lines = " ".join([f"M {x + 14 * i} {y} V {y + 140}" for i in range(1, 10)])
    h_lines = " ".join([f"M {x} {y + 14 * i} H {x + 140}" for i in range(1, 10)])
    root.add(
        Path(
            id=f"{block_id}_grid",
            d=f"{v_lines} {h_lines}",
            stroke="#D3AE1D",
            stroke_width=1,
            semantic_role="grid_lines",
        )
    )


def _add_ten_rod(root: Region, *, rod_id: str, x: float, y: float) -> None:
    root.add(
        Rect(
            id=rod_id,
            x=x,
            y=y,
            width=140,
            height=20,
            fill="#6CB5D9",
            stroke="#4B8FAF",
            stroke_width=2,
            semantic_role="ten_block",
        )
    )
    # Draw grid as a single path
    v_lines = " ".join([f"M {x + 14 * i} {y} V {y + 20}" for i in range(1, 10)])
    root.add(
        Path(
            id=f"{rod_id}_grid",
            d=v_lines,
            stroke="#4B8FAF",
            stroke_width=1,
            semantic_role="grid_lines",
        )
    )


def _add_one_unit(root: Region, *, unit_id: str, x: float, y: float) -> None:
    root.add(
        Rect(
            id=unit_id,
            x=x,
            y=y,
            width=20,
            height=20,
            fill="#E87979",
            stroke="#C95E5E",
            stroke_width=2,
            semantic_role="one_block",
        )
    )


def _add_base_ten_row(
    root: Region,
    *,
    prefix: str,
    hundreds: int,
    tens: int,
    ones: int,
    hundred_base_x: float,
    hundred_base_y: float,
    ten_base_x: float,
    ten_base_y: float,
    one_base_x: float,
    one_base_y: float,
) -> None:
    for i in range(hundreds):
        _add_hundred_block(
            root,
            block_id=f"{prefix}_{i}_hundred",
            x=hundred_base_x + (18 * i),
            y=hundred_base_y + (35 * i),
        )

    for i in range(tens):
        _add_ten_rod(
            root,
            rod_id=f"{prefix}_ten_{i}_ten",
            x=ten_base_x,
            y=ten_base_y + (24 * i),
        )

    for i in range(ones):
        _add_one_unit(
            root,
            unit_id=f"{prefix}_one_{i}_one",
            x=one_base_x + (30 * i),
            y=one_base_y,
        )


# 레이아웃 상수
def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id="0003", problem_type="base_ten_block_addition")
    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)

    root.add(
        Text(
            id="instruction",
            x=INSTRUCTION_X,
            y=INSTRUCTION_Y,
            text="수 모형으로 235+354를 구해 보세요.",
            font_size=50,
            font_family="Malgun Gothic",
            anchor="start",
            fill="#222222",
            semantic_role="instruction",
        )
    )

    root.add(
        Rect(
            id="model_box",
            x=MODEL_BOX_X,
            y=MODEL_BOX_Y,
            width=MODEL_BOX_W,
            height=MODEL_BOX_H,
            fill="none",
            stroke="#9C9CA1",
            stroke_width=3,
            semantic_role="container",
        )
    )
    root.add(
        Line(
            id="model_divider",
            x1=MODEL_BOX_X,
            y1=MODEL_DIVIDER_Y,
            x2=MODEL_BOX_X + MODEL_BOX_W,
            y2=MODEL_DIVIDER_Y,
            stroke="#9C9CA1",
            stroke_width=3,
            semantic_role="row_divider",
        )
    )

    root.add(
        Text(
            id="equation_text",
            x=EQUATION_X,
            y=EQUATION_Y,
            text="235+354=",
            font_size=56,
            font_family="Malgun Gothic",
            anchor="middle",
            fill="#222222",
            semantic_role="equation",
        )
    )
    root.add(
        Rect(
            id="answer_blank",
            x=ANSWER_BLANK_X,
            y=ANSWER_BLANK_Y,
            width=ANSWER_BLANK_W,
            height=ANSWER_BLANK_H,
            rx=10,
            fill="none",
            stroke="#69BEEA",
            stroke_width=4,
            semantic_role="answer_blank",
        )
    )

    _add_base_ten_row(root, prefix="top", **TOP_ROW)
    _add_base_ten_row(root, prefix="bottom", **BOTTOM_ROW)

    p.add(root)
    return p


from _problem_runner import save_built_problem_outputs

if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    outputs = save_built_problem_outputs(
        build(),
        current_dir,
        "0003",
        answer_semantic_path=current_dir / "0003.semantic.json",
        answer_overrides=ANSWER_LABEL_STYLE,
    )
    print("[0003] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")
