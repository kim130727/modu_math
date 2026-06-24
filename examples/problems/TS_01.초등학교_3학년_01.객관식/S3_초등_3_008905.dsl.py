from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, CircleSlot, LineSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008905",
        title="좋아하는 중국 음식",
        canvas=Canvas(width=840, height=760, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.top_caption", role="stem", flow="absolute", slot_ids=("slot.caption",)
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.frame",
                    "slot.diagram.title",
                    "slot.diagram.div_v",
                    "slot.diagram.div_h",
                    "slot.diagram.food.짜장면",
                    "slot.diagram.food.짬뽕",
                    "slot.diagram.food.볶음밥",
                    "slot.diagram.food.잡채밥",
                    "slot.diagram.legend.blue",
                    "slot.diagram.legend.red",
                    "slot.diagram.legend.blue_dot",
                    "slot.diagram.legend.red_dot",
                ),
            ),
            Region(
                id="region.table",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.table.title",
                    "slot.table.frame",
                    "slot.table.v1",
                    "slot.table.v2",
                    "slot.table.v3",
                    "slot.table.v4",
                    "slot.table.v5",
                    "slot.table.h1",
                    "slot.table.h2",
                    "slot.table.head.bg",
                    "slot.table.row1.bg",
                    "slot.table.row2.bg",
                    "slot.table.head.food",
                    "slot.table.head.jjajang",
                    "slot.table.head.jjamppong",
                    "slot.table.head.bokkeum",
                    "slot.table.head.japchae",
                    "slot.table.head.total",
                    "slot.table.row1.label",
                    "slot.table.row2.label",
                ),
            ),
            Region(
                id="region.question",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q71.checkbox", "slot.q71.text", "slot.q71.choice"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.caption",
                prompt="",
                text="준기네 반 학생들이 좋아하는 중국 음식을 조사하여 표로 나타내었습니다. 물음에 답하시오.",
                style_role="question",
                x=8.0,
                y=28.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.diagram.frame",
                prompt="",
                x=210.0,
                y=88.0,
                width=390.0,
                height=220.0,
                rx=10.0,
                ry=10.0,
            ),
            RectSlot(
                id="slot.diagram.title",
                prompt="",
                x=333.0,
                y=72.0,
                width=140.0,
                height=32.0,
                rx=0.0,
                ry=0.0,
            ),
            LineSlot(id="slot.diagram.div_v", prompt="", x1=405.0, y1=88.0, x2=405.0, y2=308.0),
            LineSlot(id="slot.diagram.div_h", prompt="", x1=210.0, y1=198.0, x2=600.0, y2=198.0),
            TextSlot(
                id="slot.diagram.food.짜장면",
                prompt="",
                text="짜장면",
                style_role="label",
                x=220.0,
                y=128.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.diagram.food.짬뽕",
                prompt="",
                text="짬뽕",
                style_role="label",
                x=417.0,
                y=128.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.diagram.food.볶음밥",
                prompt="",
                text="볶음밥",
                style_role="label",
                x=220.0,
                y=238.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.diagram.food.잡채밥",
                prompt="",
                text="잡채밥",
                style_role="label",
                x=417.0,
                y=238.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.diagram.legend.blue",
                prompt="",
                text="남학생",
                style_role="label",
                x=535.0,
                y=332.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.diagram.legend.red",
                prompt="",
                text="여학생",
                style_role="label",
                x=605.0,
                y=332.0,
                font_size=22,
            ),
            CircleSlot(
                id="slot.diagram.legend.blue_dot",
                prompt="",
                cx=523.0,
                cy=325.0,
                r=7.0,
                fill="#7EC9F6",
            ),
            CircleSlot(
                id="slot.diagram.legend.red_dot",
                prompt="",
                cx=594.0,
                cy=325.0,
                r=7.0,
                fill="#F6A19A",
            ),
            CircleSlot(
                id="slot.diagram.dot.b1", prompt="", cx=255.0, cy=135.0, r=8.0, fill="#7EC9F6"
            ),
            CircleSlot(
                id="slot.diagram.dot.b2", prompt="", cx=280.0, cy=165.0, r=8.0, fill="#7EC9F6"
            ),
            CircleSlot(
                id="slot.diagram.dot.b3", prompt="", cx=310.0, cy=165.0, r=8.0, fill="#7EC9F6"
            ),
            CircleSlot(
                id="slot.diagram.dot.b4", prompt="", cx=340.0, cy=165.0, r=8.0, fill="#7EC9F6"
            ),
            CircleSlot(
                id="slot.diagram.dot.b5", prompt="", cx=370.0, cy=165.0, r=8.0, fill="#7EC9F6"
            ),
            CircleSlot(
                id="slot.diagram.dot.r1", prompt="", cx=300.0, cy=135.0, r=8.0, fill="#F6A19A"
            ),
            CircleSlot(
                id="slot.diagram.dot.r2", prompt="", cx=345.0, cy=135.0, r=8.0, fill="#F6A19A"
            ),
            CircleSlot(
                id="slot.diagram.dot.r3", prompt="", cx=445.0, cy=135.0, r=8.0, fill="#F6A19A"
            ),
            CircleSlot(
                id="slot.diagram.dot.r4", prompt="", cx=492.0, cy=122.0, r=8.0, fill="#F6A19A"
            ),
            CircleSlot(
                id="slot.diagram.dot.r5", prompt="", cx=525.0, cy=123.0, r=8.0, fill="#F6A19A"
            ),
            CircleSlot(
                id="slot.diagram.dot.r6", prompt="", cx=545.0, cy=121.0, r=8.0, fill="#F6A19A"
            ),
            CircleSlot(
                id="slot.diagram.dot.r7", prompt="", cx=445.0, cy=170.0, r=8.0, fill="#F6A19A"
            ),
            CircleSlot(
                id="slot.diagram.dot.r8", prompt="", cx=482.0, cy=170.0, r=8.0, fill="#F6A19A"
            ),
            CircleSlot(
                id="slot.diagram.dot.r9", prompt="", cx=532.0, cy=171.0, r=8.0, fill="#F6A19A"
            ),
            CircleSlot(
                id="slot.diagram.dot.b6", prompt="", cx=488.0, cy=145.0, r=8.0, fill="#7EC9F6"
            ),
            CircleSlot(
                id="slot.diagram.dot.b7", prompt="", cx=530.0, cy=143.0, r=8.0, fill="#7EC9F6"
            ),
            CircleSlot(
                id="slot.diagram.dot.b8", prompt="", cx=510.0, cy=168.0, r=8.0, fill="#7EC9F6"
            ),
            CircleSlot(
                id="slot.diagram.dot.b9", prompt="", cx=280.0, cy=266.0, r=8.0, fill="#7EC9F6"
            ),
            CircleSlot(
                id="slot.diagram.dot.b10", prompt="", cx=320.0, cy=252.0, r=8.0, fill="#7EC9F6"
            ),
            CircleSlot(
                id="slot.diagram.dot.r10", prompt="", cx=317.0, cy=282.0, r=8.0, fill="#F6A19A"
            ),
            CircleSlot(
                id="slot.diagram.dot.r11", prompt="", cx=353.0, cy=252.0, r=8.0, fill="#F6A19A"
            ),
            CircleSlot(
                id="slot.diagram.dot.r12", prompt="", cx=353.0, cy=282.0, r=8.0, fill="#F6A19A"
            ),
            CircleSlot(
                id="slot.diagram.dot.b11", prompt="", cx=458.0, cy=256.0, r=8.0, fill="#7EC9F6"
            ),
            CircleSlot(
                id="slot.diagram.dot.b12", prompt="", cx=505.0, cy=255.0, r=8.0, fill="#7EC9F6"
            ),
            CircleSlot(
                id="slot.diagram.dot.r13", prompt="", cx=479.0, cy=279.0, r=8.0, fill="#F6A19A"
            ),
            CircleSlot(
                id="slot.diagram.dot.r14", prompt="", cx=527.0, cy=278.0, r=8.0, fill="#F6A19A"
            ),
            RectSlot(
                id="slot.table.title",
                prompt="",
                x=250.0,
                y=370.0,
                width=240.0,
                height=32.0,
                rx=0.0,
                ry=0.0,
            ),
            RectSlot(
                id="slot.table.frame",
                prompt="",
                x=110.0,
                y=410.0,
                width=620.0,
                height=112.0,
                rx=0.0,
                ry=0.0,
            ),
            LineSlot(id="slot.table.v1", prompt="", x1=238.0, y1=410.0, x2=238.0, y2=522.0),
            LineSlot(id="slot.table.v2", prompt="", x1=332.0, y1=410.0, x2=332.0, y2=522.0),
            LineSlot(id="slot.table.v3", prompt="", x1=426.0, y1=410.0, x2=426.0, y2=522.0),
            LineSlot(id="slot.table.v4", prompt="", x1=520.0, y1=410.0, x2=520.0, y2=522.0),
            LineSlot(id="slot.table.v5", prompt="", x1=614.0, y1=410.0, x2=614.0, y2=522.0),
            LineSlot(id="slot.table.h1", prompt="", x1=110.0, y1=444.0, x2=730.0, y2=444.0),
            LineSlot(id="slot.table.h2", prompt="", x1=110.0, y1=478.0, x2=730.0, y2=478.0),
            RectSlot(
                id="slot.table.head.bg",
                prompt="",
                x=110.0,
                y=410.0,
                width=620.0,
                height=34.0,
                rx=0.0,
                ry=0.0,
            ),
            RectSlot(
                id="slot.table.row1.bg",
                prompt="",
                x=110.0,
                y=444.0,
                width=620.0,
                height=34.0,
                rx=0.0,
                ry=0.0,
            ),
            RectSlot(
                id="slot.table.row2.bg",
                prompt="",
                x=110.0,
                y=478.0,
                width=620.0,
                height=34.0,
                rx=0.0,
                ry=0.0,
            ),
            TextSlot(
                id="slot.table.head.food",
                prompt="",
                text="음식",
                style_role="label",
                x=156.0,
                y=433.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.table.head.jjajang",
                prompt="",
                text="짜장면",
                style_role="label",
                x=262.0,
                y=433.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.table.head.jjamppong",
                prompt="",
                text="짬뽕",
                style_role="label",
                x=365.0,
                y=433.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.table.head.bokkeum",
                prompt="",
                text="볶음밥",
                style_role="label",
                x=454.0,
                y=433.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.table.head.japchae",
                prompt="",
                text="잡채밥",
                style_role="label",
                x=550.0,
                y=433.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.table.head.total",
                prompt="",
                text="합계",
                style_role="label",
                x=645.0,
                y=433.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.table.row1.label",
                prompt="",
                text="남학생 수(명)",
                style_role="label",
                x=128.0,
                y=467.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.table.row2.label",
                prompt="",
                text="여학생 수(명)",
                style_role="label",
                x=128.0,
                y=501.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.q71.checkbox",
                prompt="",
                text="□",
                style_role="question",
                x=14.0,
                y=565.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.q71.text",
                prompt="",
                text="71. 준기네 반에서 중국 음식을 한 가지만 주문한다면 어떤 음식을 주문하면\n좋을까요? 알맞은 것을 선택해보세요.",
                style_role="question",
                x=40.0,
                y=568.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q71.choice",
                prompt="",
                text="( 짜장면 , 짬뽕 , 볶음밥 , 잡채밥 )",
                style_role="question",
                x=500.0,
                y=636.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008905",
    "problem_type": "표 읽기",
    "metadata": {
        "language": "ko",
        "question": "준기네 반에서 중국 음식을 한 가지만 주문한다면 어떤 음식을 주문하면 좋을까요?",
        "instruction": "알맞은 것을 선택하시오.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.foods",
                "type": "category_set",
                "items": ["짜장면", "짬뽕", "볶음밥", "잡채밥"],
            },
            {"id": "obj.chart", "type": "survey_chart", "topic": "좋아하는 중국 음식"},
            {"id": "obj.table", "type": "frequency_table", "topic": "좋아하는 중국 음식별 학생 수"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.chart", "obj.table"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.chart_table_correspondence", "rel.ask_most_preferred"],
            },
            "plan": {
                "method": "표와 그림 자료 읽기",
                "description": "그림과 표를 대응시켜 각 음식의 선호를 비교한 뒤 알맞은 선택지를 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "diagram_table_matching",
                    "compare_categories",
                    "choose_best_option",
                ]
            },
            "review": {
                "check_methods": ["choice_consistency_check", "table_diagram_consistency_check"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "most_preferred_food",
            "description": "한 가지만 주문한다면 알맞은 중국 음식",
        },
        "value": "짬뽕",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008905",
    "problem_type": "표 읽기",
    "inputs": {
        "total_ticks": 0,
        "target_label": "가장 많이 좋아하는 중국 음식",
        "target_ticks": 0,
        "target_count": 0,
        "unit": "",
    },
    "given": [
        {"ref": "obj.chart", "value": {"topic": "좋아하는 중국 음식"}},
        {"ref": "obj.table", "value": {"topic": "좋아하는 중국 음식별 학생 수"}},
    ],
    "target": {"ref": "answer.target", "type": "most_preferred_food"},
    "method": "표와 그림 자료 읽기",
    "plan": ["그림과 표의 대응 관계를 확인한다.", "보기 중 알맞은 음식을 찾는다."],
    "steps": [
        {
            "id": "step.1",
            "expr": "문항에서 고르려는 대상 확인",
            "value": "한 가지만 주문할 중국 음식",
        },
        {"id": "step.2", "expr": "보기 확인", "value": ["짜장면", "짬뽕", "볶음밥", "잡채밥"]},
        {"id": "step.3", "expr": "이미지에 인쇄된 정답 확인", "value": "짬뽕"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "정답 텍스트가 이미지에 보이는가",
            "expected": "짬뽕",
            "actual": "짬뽕",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "most_preferred_food",
            "description": "한 가지만 주문한다면 알맞은 중국 음식",
        },
        "value": "짬뽕",
        "unit": "",
    },
}
