from pathlib import Path
import sys

from modu_semantic import Circle, Line, Problem, Rect, Region, Text

# 0010: 덧셈 기계 표 완성하기
CANVAS_W = 1498
CANVAS_H = 644

INSTRUCTION_TEXT = "빈칸에 알맞은 수를 써 넣으세요."
INSTRUCTION_X = 28
INSTRUCTION_Y = 106.44896

ARROW_X1 = 317.18445
ARROW_Y = 228.24083
ARROW_X2 = 910.18445
ARROW_HEAD_X = 880.18445
ARROW_HEAD_Y1 = 198.24083
ARROW_HEAD_Y2 = 258.24084

PLUS_CX = 614.18445
PLUS_CY = 228.24083
PLUS_R = 48

TABLE_X = 319.18445
TABLE_Y = 298.24084
TABLE_W = 888
TABLE_H = 279

V1_X = 616.18445
V2_X = 909.18445
H1_Y = 437.24084

R1C1_X = 468.18445
R1C2_X = 761.18445
R1_Y = 392.24084
R2_Y = 528.24084

R1_BLANK_X = 939.18445
R1_BLANK_Y = 329.24084
R2_BLANK_X = 939.18445
R2_BLANK_Y = 465.24084
BLANK_W = 238
BLANK_H = 78


def build() -> Problem:
    p = Problem(width=CANVAS_W, height=CANVAS_H, problem_id="0010", problem_type="table_addition_machine")
    p.title = "덧셈 기계"

    p.set_domain(
        {
            "instruction": INSTRUCTION_TEXT,
            "operator": "+",
            "rows": [
                {"left": 467, "middle": 359, "right": 826},
                {"left": 735, "middle": 418, "right": 1153},
            ],
        }
    )
    p.set_answer(
        blanks=[
            {"id": "r1_blank", "kind": "numeric", "value": "826"},
            {"id": "r2_blank", "kind": "numeric", "value": "1153"},
        ],
        choices=[],
        answer_key=[
            {"target": "r1_blank", "value": "826"},
            {"target": "r2_blank", "value": "1153"},
        ],
    )

    root = Region(id="problem_root", x=0, y=0, width=CANVAS_W, height=CANVAS_H, visible_debug=False)

    # 문제 문장
    root.add(
        Text(
            id="inst",
            x=INSTRUCTION_X,
            y=INSTRUCTION_Y,
            text=INSTRUCTION_TEXT,
            font_size=72,
            font_family="Malgun Gothic",
            fill="#222222",
            anchor="start",
            semantic_role="instruction",
        )
    )

    # 화살표 + 연산자
    root.add(
        Line(
            id="arrow",
            x1=ARROW_X1,
            y1=ARROW_Y,
            x2=ARROW_X2,
            y2=ARROW_Y,
            stroke="#CCCED2",
            stroke_width=22,
            semantic_role="flow_arrow",
        )
    )
    root.add(
        Line(
            id="arrow_head1",
            x1=ARROW_X2,
            y1=ARROW_Y,
            x2=ARROW_HEAD_X,
            y2=ARROW_HEAD_Y1,
            stroke="#CCCED2",
            stroke_width=22,
            semantic_role="flow_arrow",
        )
    )
    root.add(
        Line(
            id="arrow_head2",
            x1=ARROW_X2,
            y1=ARROW_Y,
            x2=ARROW_HEAD_X,
            y2=ARROW_HEAD_Y2,
            stroke="#CCCED2",
            stroke_width=22,
            semantic_role="flow_arrow",
        )
    )
    root.add(
        Circle(
            id="plus_circle",
            cx=PLUS_CX,
            cy=PLUS_CY,
            r=PLUS_R,
            fill="#F6F6F6",
            stroke="#B9D8DA",
            stroke_width=10,
            semantic_role="operator",
        )
    )
    root.add(
        Line(
            id="plus_h",
            x1=PLUS_CX - 25,
            y1=PLUS_CY,
            x2=PLUS_CX + 25,
            y2=PLUS_CY,
            stroke="#3A3338",
            stroke_width=4,
            semantic_role="operator",
        )
    )
    root.add(
        Line(
            id="plus_v",
            x1=PLUS_CX,
            y1=PLUS_CY - 25,
            x2=PLUS_CX,
            y2=PLUS_CY + 25,
            stroke="#3A3338",
            stroke_width=4,
            semantic_role="operator",
        )
    )

    # 표
    root.add(
        Rect(
            id="table",
            x=TABLE_X,
            y=TABLE_Y,
            width=TABLE_W,
            height=TABLE_H,
            fill="none",
            stroke="#B9D8DA",
            stroke_width=9,
            semantic_role="table",
        )
    )
    root.add(
        Line(
            id="v1",
            x1=V1_X,
            y1=TABLE_Y,
            x2=V1_X,
            y2=TABLE_Y + TABLE_H,
            stroke="#B9D8DA",
            stroke_width=4,
            semantic_role="table_grid",
        )
    )
    root.add(
        Line(
            id="v2",
            x1=V2_X,
            y1=TABLE_Y,
            x2=V2_X,
            y2=TABLE_Y + TABLE_H,
            stroke="#B9D8DA",
            stroke_width=4,
            semantic_role="table_grid",
        )
    )
    root.add(
        Line(
            id="h1",
            x1=TABLE_X,
            y1=H1_Y,
            x2=TABLE_X + TABLE_W,
            y2=H1_Y,
            stroke="#B9D8DA",
            stroke_width=4,
            semantic_role="table_grid",
        )
    )

    # 표 내부 숫자
    root.add(
        Text(
            id="r1c1",
            x=R1C1_X,
            y=R1_Y,
            text="467",
            font_size=68,
            font_family="Cambria",
            fill="#222222",
            anchor="middle",
            semantic_role="table_value",
        )
    )
    root.add(
        Text(
            id="r1c2",
            x=R1C2_X,
            y=R1_Y,
            text="359",
            font_size=68,
            font_family="Cambria",
            fill="#222222",
            anchor="middle",
            semantic_role="table_value",
        )
    )
    root.add(
        Text(
            id="r2c1",
            x=R1C1_X,
            y=R2_Y,
            text="735",
            font_size=68,
            font_family="Cambria",
            fill="#222222",
            anchor="middle",
            semantic_role="table_value",
        )
    )
    root.add(
        Text(
            id="r2c2",
            x=R1C2_X,
            y=R2_Y,
            text="418",
            font_size=68,
            font_family="Cambria",
            fill="#222222",
            anchor="middle",
            semantic_role="table_value",
        )
    )

    # 정답 칸(문제 SVG에서는 빈칸으로 유지)
    root.add(
        Rect(
            id="r1_blank",
            x=R1_BLANK_X,
            y=R1_BLANK_Y,
            width=BLANK_W,
            height=BLANK_H,
            rx=10,
            fill="none",
            stroke="#69BEEA",
            stroke_width=4,
            semantic_role="answer_blank",
        )
    )
    root.add(
        Rect(
            id="r2_blank",
            x=R2_BLANK_X,
            y=R2_BLANK_Y,
            width=BLANK_W,
            height=BLANK_H,
            rx=10,
            fill="none",
            stroke="#69BEEA",
            stroke_width=4,
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
        "0010",
        answer_semantic_path=CURRENT_DIR / "input" / "json" / "semantic_final.json",
    )
    print("[0010] generated:")
    print(f"  - {outputs['problem_svg']}")
    print(f"  - {outputs['answer_svg']}")
