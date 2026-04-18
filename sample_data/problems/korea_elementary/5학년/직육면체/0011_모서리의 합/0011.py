from pathlib import Path
import sys

from modu_semantic import Line, Problem, Rect, Region, Text

CANVAS_W = 608
CANVAS_H = 580

ANSWER_LABEL_STYLE = {
    "use_answer_label": True,
    "answer_label_top_right": False,
    "answer_label_x": 46,
    "answer_label_y": 564,
    "answer_label_anchor": "start",
    "answer_label_baseline": "auto",
    "answer_label_font_size": 34,
    "explain_x": 46,
    "explain_font_size": 19,
    "explain_line_height": 24,
    "explain_bottom_margin": 112,
}


def _wrap_line_by_width(text: str, *, max_width: float, font_size: float) -> list[str]:
    if not text:
        return [""]

    # 한글/영문 혼합 문장에서 우측 침범을 줄이기 위해 보수적으로 폭을 계산한다.
    approx_char_width = font_size * 0.66
    max_chars = max(1, int(max_width / approx_char_width))

    words = text.split(" ")
    lines: list[str] = []
    current = ""

    for word in words:
        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
            continue

        if current:
            lines.append(current)
            current = word
            continue

        # 단일 토큰이 너무 긴 경우 문자 단위 분할
        for i in range(0, len(word), max_chars):
            chunk = word[i : i + max_chars]
            if len(chunk) == max_chars:
                lines.append(chunk)
            else:
                current = chunk

    if current:
        lines.append(current)

    return lines or [text]


def _wrap_lines(lines: list[str], *, max_width: float, font_size: float) -> list[str]:
    wrapped: list[str] = []
    for line in lines:
        wrapped.extend(_wrap_line_by_width(line, max_width=max_width, font_size=font_size))
    return wrapped


def _add_text_lines(
    root: Region,
    lines: list[str],
    *,
    x: float,
    y: float,
    step: float,
    prefix: str,
    font_size: int = 17,
) -> None:
    for i, line in enumerate(lines):
        root.add(
            Text(
                id=f"{prefix}_{i+1}",
                x=x,
                y=y + (i * step),
                text=line,
                font_size=font_size,
                font_family="Malgun Gothic",
                fill="#222222",
                anchor="start",
                semantic_role="instruction",
            )
        )


def _add_cube_with_cut(
    root: Region,
    *,
    prefix: str,
    ox: float,
    oy: float,
    side: float = 115.4,
    dx: float = 38.5,
    dy: float = -32.7,
    edge_color: str = "#333333",
    truncate_corner_edges: bool = False,
) -> None:
    # 앞면 꼭짓점
    flt = (ox, oy)
    frt = (ox + side, oy)
    flb = (ox, oy + side)
    frb = (ox + side, oy + side)

    # 뒷면 꼭짓점
    blt = (ox + dx, oy + dy)
    brt = (ox + side + dx, oy + dy)
    blb = (ox + dx, oy + side + dy)
    brb = (ox + side + dx, oy + side + dy)

    def add_edge(eid: str, a: tuple[float, float], b: tuple[float, float], dashed: bool = False, w: float = 1.3) -> None:
        style = {"stroke_dasharray": "4 4"} if dashed else {}
        root.add(
            Line(
                id=f"{prefix}_{eid}",
                x1=a[0],
                y1=a[1],
                x2=b[0],
                y2=b[1],
                stroke=edge_color,
                stroke_width=w,
                semantic_role="decorative",
                metadata=style,
            )
        )

    # 잘린 면(삼각형)
    cut_a = (ox + side * 0.52, oy + side * 0.00)
    cut_b = (ox + side * 1.00, oy + side * 0.42)
    cut_c = (ox + side * 1.15, oy + side * -0.13)

    # 큐브 기본 선
    # 우측 도형은 ㄱㅇ/ㄷㅇ/ㅁㅇ 선분을 절단면 꼭짓점까지만 연결한다.
    if truncate_corner_edges:
        add_edge("front_top", flt, cut_a, w=0.95)      # ㄱㅇ
        add_edge("front_right", cut_b, frb, w=0.95)    # ㅁㅇ
        add_edge("connect_rt", cut_c, brt, w=0.70)     # ㄷㅇ
    else:
        add_edge("front_top", flt, frt)
        add_edge("front_right", frt, frb)
        add_edge("connect_rt", frt, brt)

    add_edge("front_bottom", flb, frb)
    add_edge("front_left", flt, flb)

    add_edge("back_top", blt, brt)
    add_edge("back_right", brt, brb)

    add_edge("connect_lt", flt, blt)
    add_edge("connect_rb", frb, brb)

    add_edge("back_left_hidden", blt, blb, dashed=True)
    add_edge("back_bottom_hidden", blb, brb, dashed=True)
    add_edge("connect_lb_hidden", flb, blb, dashed=True)

    add_edge("cut_ab", cut_a, cut_b, w=1.5)
    add_edge("cut_ac", cut_a, cut_c, w=0.9)
    add_edge("cut_bc", cut_b, cut_c, w=0.9)

    # 꼭짓점 라벨
    labels = [
        ("A", (flt[0] - 11, flt[1] + 5)),
        ("B", (blt[0] - 14, blt[1] + 14)),
        ("C", (brt[0] + 12, brt[1] - 2)),
        ("D", (flb[0] - 6, flb[1] + 14)),
        ("E", (frb[0] + 2, frb[1] + 14)),
        ("F", (brb[0] + 12, brb[1] + 8)),
        ("G", (blb[0] + 6, blb[1] + 12)),
        ("O", (frt[0] - 10, frt[1] + 14)),
    ]
    if truncate_corner_edges:
        labels = labels[:-1]
    for i, (ch, (x, y)) in enumerate(labels):
        root.add(
            Text(
                id=f"{prefix}_lbl_{i+1}",
                x=x,
                y=y,
                text=ch,
                font_size=16,
                font_family="Malgun Gothic",
                fill="#222222",
                anchor="middle",
                semantic_role="vertex_label",
            )
        )


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id="0011", problem_type="cube_corner_cut_edges_sum")
    p.title = "정육면체 모서리 길이의 합"

    top_lines = [
        "모든 면이 정사각형이고 한 면의 넓이가 8 cm²인 사각기둥이 있습니다. [보기]는 이 사각기둥에서 ㄴ을 각뿔의 꼭짓점으로 하는 삼각뿔 모양을 자른 것입니다.",
    ]
    question_lines = [
        "[보기]와 같은 방법으로 처음 사각기둥에서 각각 꼭짓점 B, O, D, F을 각뿔의 꼭젓점으로 하는 삼각뿔 모양 4개를 자르려고 합니다. 가장 큰 삼각뿔 모양이 되도록 모두 잘랐을 때 자르고 남은 도형의 모든 모서리의 길이의 합은 몇 cm입니까?",
    ]

    p.set_domain(
        {
            "instruction_lines": top_lines,
            "question_lines": question_lines,
            "given_face_area_cm2": 8,
            "cut_corner_count": 4,
            "computed_answer": "12+12√2",
            "solution_strategy": "새 모서리 6개와 잘리고 남은 기존 모서리를 모두 더한다.",
            "answer_explanation_lines": [
                "풀이: a^2=8 이므로 a=2√2",
                "새 모서리 6개: AC=CE=...=2cm -> 6*2=12",
                "남은 기존 모서리 12개: 각 a/2=√2 -> 12√2",
                "합계: 12 + 12√2",
            ],
        }
    )
    p.set_answer(
        blanks=[{"id": "ans_blank", "kind": "expression", "value": "12+12√2"}],
        choices=[],
        answer_key=[{"target": "ans_blank", "value": "12+12√2"}],
    )

    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)

    top_wrapped = _wrap_lines(top_lines, max_width=450, font_size=17)
    _add_text_lines(root, top_wrapped, x=45, y=36, step=28, prefix="inst", font_size=17)
    example_tag_y = 36 + (len(top_wrapped) * 28) + 24

    root.add(
        Text(
            id="example_tag",
            x=58,
            y=example_tag_y,
            text="[보기]",
            font_size=17,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="label",
        )
    )

    _add_cube_with_cut(root, prefix="cube_l", ox=91, oy=210)

    root.add(
        Line(
            id="arrow_body",
            x1=291,
            y1=256,
            x2=311,
            y2=256,
            stroke="#333333",
            stroke_width=2,
            semantic_role="flow_arrow",
        )
    )
    root.add(
        Line(
            id="arrow_head_u",
            x1=311,
            y1=256,
            x2=305,
            y2=250,
            stroke="#333333",
            stroke_width=2,
            semantic_role="flow_arrow",
        )
    )
    root.add(
        Line(
            id="arrow_head_d",
            x1=311,
            y1=256,
            x2=305,
            y2=262,
            stroke="#333333",
            stroke_width=2,
            semantic_role="flow_arrow",
        )
    )

    _add_cube_with_cut(root, prefix="cube_r", ox=358, oy=212, truncate_corner_edges=True)

    question_wrapped = _wrap_lines(question_lines, max_width=450, font_size=17)
    _add_text_lines(root, question_wrapped, x=48, y=383, step=29, prefix="q", font_size=17)

    # 답 칸
    root.add(
        Text(
            id="ans_l",
            x=398,
            y=512,
            text="(",
            font_size=28,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="middle",
            semantic_role="answer_blank",
        )
    )
    root.add(
        Rect(
            id="ans_blank",
            x=420,
            y=488,
            width=110,
            height=34,
            rx=4,
            fill="none",
            stroke="#69BEEA",
            stroke_width=2,
            semantic_role="answer_blank",
        )
    )
    root.add(
        Text(
            id="ans_r",
            x=558,
            y=512,
            text=") cm",
            font_size=28,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="middle",
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
        "0011",
        answer_semantic_path=CURRENT_DIR / "input" / "json" / "semantic_final.json",
        answer_overrides=ANSWER_LABEL_STYLE,
    )
    print("[0011] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")
