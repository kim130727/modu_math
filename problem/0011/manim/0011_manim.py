from __future__ import annotations

import sys
from pathlib import Path

from manim import Scene

sys.dont_write_bytecode = True


def _ensure_repo_root_on_path() -> None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "problem").is_dir() and (parent / "README.md").exists():
            root = str(parent)
            if root not in sys.path:
                sys.path.insert(0, root)
            return
    raise RuntimeError("Repository root could not be resolved from current file path.")


_ensure_repo_root_on_path()

from problem.common.manim_renderer import render_manim_from_semantic
from problem.common.problem_cli import configure_manim_output_dirs, load_problem_data, run_cli, validate_or_raise

configure_manim_output_dirs(Path(__file__))


LINE = "#333333"
BG = "#F6F6F6"


def add_line(elements: list[dict], id_: str, x1: float, y1: float, x2: float, y2: float, dash: str | None = None, stroke_width: int = 2) -> None:
    row = {
        "id": id_,
        "type": "line",
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "stroke": LINE,
        "stroke_width": stroke_width,
    }
    if dash:
        row["dasharray"] = dash
    elements.append(row)


def add_text(elements: list[dict], id_: str, text: str, x: float, y: float, font_size: int = 28, anchor: str = "middle") -> None:
    elements.append(
        {
            "id": id_,
            "type": "text",
            "text": text,
            "x": x,
            "y": y,
            "anchor": anchor,
            "font_family": "Malgun Gothic",
            "font_size": font_size,
            "fill": "#222222",
        }
    )


def draw_left_shape(elements: list[dict]) -> None:
    # first code (left)
    FLT = (180, 220)   # ㄱ
    FRT = (360, 220)
    FRB = (360, 400)   # ㅂ
    FLB = (180, 400)   # ㅁ

    dx, dy = 60, -50
    BLT = (FLT[0] + dx, FLT[1] + dy)   # ㄹ
    BRT = (FRT[0] + dx, FRT[1] + dy)   # ㄷ
    BRB = (FRB[0] + dx, FRB[1] + dy)   # ㅅ
    BLB = (FLB[0] + dx, FLB[1] + dy)   # ㅇ

    add_line(elements, "l_front_top", *FLT, *FRT)
    add_line(elements, "l_front_right", *FRT, *FRB)
    add_line(elements, "l_front_bottom", *FLB, *FRB)
    add_line(elements, "l_front_left", *FLT, *FLB)

    add_line(elements, "l_back_top", *BLT, *BRT)
    add_line(elements, "l_back_right", *BRT, *BRB)

    add_line(elements, "l_connect_lt", *FLT, *BLT)
    add_line(elements, "l_connect_rt", *FRT, *BRT)
    add_line(elements, "l_connect_rb", *FRB, *BRB)

    add_line(elements, "l_back_left_hidden", *BLT, *BLB, dash="4 4")
    add_line(elements, "l_back_bottom_hidden", *BLB, *BRB, dash="4 4")
    add_line(elements, "l_connect_lb_hidden", *FLB, *BLB, dash="4 4")

    cut_a = (300, 220)
    cut_b = (360, 295)
    cut_c = (420, 170)

    add_line(elements, "l_cut_ab", *cut_a, *cut_b)
    add_line(elements, "l_cut_ac", *cut_a, *cut_c)
    add_line(elements, "l_cut_bc", *cut_b, *cut_c)

    inner = (350, 255)
    add_line(elements, "l_inner_a", inner[0], inner[1], cut_a[0], cut_a[1])
    add_line(elements, "l_inner_b", inner[0], inner[1], cut_b[0], cut_b[1])
    add_line(elements, "l_inner_c", inner[0], inner[1], cut_c[0], cut_c[1])

    add_text(elements, "l_lbl_ㄱ", "ㄱ", FLT[0] - 18, FLT[1] + 4, font_size=26)
    add_text(elements, "l_lbl_ㄹ", "ㄹ", BLT[0], BLT[1] - 16, font_size=26)
    add_text(elements, "l_lbl_ㄷ", "ㄷ", BRT[0] + 12, BRT[1] - 2, font_size=26)
    add_text(elements, "l_lbl_ㅁ", "ㅁ", FLB[0] - 14, FLB[1] + 16, font_size=26)
    add_text(elements, "l_lbl_ㅂ", "ㅂ", FRB[0] + 8, FRB[1] + 16, font_size=26)
    add_text(elements, "l_lbl_ㅅ", "ㅅ", BRB[0] + 16, BRB[1] + 2, font_size=26)
    add_text(elements, "l_lbl_ㅇ", "ㅇ", BLB[0] - 2, BLB[1] + 10, font_size=26)
    add_text(elements, "l_lbl_ㄴ", "ㄴ", inner[0] + 18, inner[1] - 4, font_size=26)


def draw_right_shape(elements: list[dict], sx: float = 430, k: float = 0.55) -> None:
    # second code (right), scaled and shifted for side-by-side layout
    def tx(x: float) -> float:
        return sx + (x - 120) * k

    def ty(y: float) -> float:
        return 220 + (y - 220) * k

    A = (tx(120), ty(220))   # ㄱ
    B = (tx(300), ty(220))
    C = (tx(300), ty(400))   # ㅂ
    D = (tx(120), ty(400))   # ㅁ

    dx, dy = 68 * k, -52 * k
    E = (A[0] + dx, A[1] + dy)   # ㄹ
    F = (B[0] + dx, B[1] + dy)   # ㄷ
    G = (C[0] + dx, C[1] + dy)   # ㅅ
    H = (D[0] + dx, D[1] + dy)   # ㅇ

    add_line(elements, "r_front_top", *A, *B)
    add_line(elements, "r_front_right", *B, *C)
    add_line(elements, "r_front_bottom", *D, *C)
    add_line(elements, "r_front_left", *A, *D)

    add_line(elements, "r_back_top", *E, *F)
    add_line(elements, "r_back_right", *F, *G)
    add_line(elements, "r_connect_left_top", *A, *E)
    add_line(elements, "r_connect_right_top", *B, *F)
    add_line(elements, "r_connect_right_bottom", *C, *G)

    add_line(elements, "r_hidden_back_left", *E, *H, dash="4 4")
    add_line(elements, "r_hidden_back_bottom", *H, *G, dash="4 4")
    add_line(elements, "r_hidden_left_depth", *D, *H, dash="4 4")

    P = (tx(220), ty(220))
    Q = (tx(300), ty(288))
    R = (tx(368), ty(168))

    add_line(elements, "r_cut_top", *P, *R)
    add_line(elements, "r_cut_left", *P, *Q)
    add_line(elements, "r_cut_right", *R, *Q)

    add_text(elements, "r_lbl_ㄱ", "ㄱ", A[0] - 16, A[1] + 2, font_size=26)
    add_text(elements, "r_lbl_ㄹ", "ㄹ", E[0] - 4, E[1] - 14, font_size=26)
    add_text(elements, "r_lbl_ㄷ", "ㄷ", F[0] + 14, F[1] - 2, font_size=26)
    add_text(elements, "r_lbl_ㅁ", "ㅁ", D[0] - 12, D[1] + 18, font_size=26)
    add_text(elements, "r_lbl_ㅂ", "ㅂ", C[0] + 8, C[1] + 18, font_size=26)
    add_text(elements, "r_lbl_ㅅ", "ㅅ", G[0] + 16, G[1] + 2, font_size=26)
    add_text(elements, "r_lbl_ㅇ", "ㅇ", H[0] - 2, H[1] + 12, font_size=26)
    add_text(elements, "r_lbl_ㄴ", "ㄴ", tx(284), ty(264), font_size=26)


def create_semantic_payload(data: dict) -> dict:
    problem_id = f"{int(data['id']):04d}"
    elements: list[dict] = []

    # Header & container
    add_text(elements, "num", "8", 16, 54, font_size=56, anchor="start")
    elements[-1]["fill"] = "#6F3FA2"

    add_text(elements, "inst_l1", "모든 면이 정사각형이고 한 면의 넓이가 8 cm^2인", 58, 42, font_size=24, anchor="start")
    add_text(elements, "inst_l2", "사각기둥이 있습니다. [보기]는 이 사각기둥에서 꼭짓점", 16, 82, font_size=24, anchor="start")
    add_text(elements, "inst_l3", "ㄴ을 각뿔의 꼭짓점으로 하는 삼각뿔 모양을 자른 것입", 16, 122, font_size=24, anchor="start")
    add_text(elements, "inst_l4", "니다.", 16, 162, font_size=24, anchor="start")

    elements.append(
        {
            "id": "example_box",
            "type": "rect",
            "x": 64,
            "y": 166,
            "width": 470,
            "height": 220,
            "rx": 12,
            "stroke": "#8A8A8A",
            "stroke_width": 1.5,
            "fill": "none",
        }
    )
    add_text(elements, "example_label", "[보기]", 84, 170, font_size=42, anchor="start")

    # Left / right shapes from your two code boxes
    draw_left_shape(elements)

    add_line(elements, "arr_1", 405, 286, 425, 286, stroke_width=2)
    add_line(elements, "arr_2", 425, 286, 419, 280, stroke_width=2)
    add_line(elements, "arr_3", 425, 286, 419, 292, stroke_width=2)

    draw_right_shape(elements)

    add_line(elements, "right_bar", 538, 338, 538, 352, stroke_width=2)

    add_text(elements, "q1", "[보기]와 같은 방법으로 처음 사각기둥에서 각각 꼭짓점", 16, 422, font_size=24, anchor="start")
    add_text(elements, "q2", "ㄴ, ㄹ, ㅁ, ㅅ을 각뿔의 꼭짓점으로 하는 삼각뿔 모양 4", 16, 462, font_size=24, anchor="start")
    add_text(elements, "q3", "개를 자르려고 합니다. 가장 큰 삼각뿔 모양이 되도록 모", 16, 502, font_size=24, anchor="start")
    add_text(elements, "q4", "두 잘랐을 때 자르고 남은 도형의 모든 모서리의 길이의", 16, 542, font_size=24, anchor="start")
    add_text(elements, "q5", "합은 몇 cm입니까?", 16, 576, font_size=24, anchor="start")

    add_text(elements, "ans_l", "(", 330, 564, font_size=40)
    add_text(elements, "ans_r", ")", 560, 564, font_size=40)

    return {
        "meta": {
            "schema": "modu_math.semantic.v2",
            "problem_id": problem_id,
            "source": f"problem/{problem_id}/manim/{problem_id}_manim.py",
        },
        "problem": data,
        "canvas": {"width": 608, "height": 580, "background": BG},
        "elements": elements,
    }


class CubeStepMerged(Scene):
    def construct(self) -> None:
        semantic = create_semantic_payload(load_problem_data(Path(__file__)))
        validate_or_raise(semantic)
        render_manim_from_semantic(self, semantic)
        self.wait(2)


SceneClass = CubeStepMerged

if __name__ == "__main__":
    run_cli(Path(__file__), create_semantic_payload)
