from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008921",
        title="마을별 병원 수 그림그래프",
        canvas=Canvas(width=960.0, height=540.0, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1", "slot.q2")),
            Region(
                id="region.chart",
                role="body",
                flow="absolute",
                slot_ids=(
                    "slot.title",
                    "slot.table.outer",
                    "slot.table.head1",
                    "slot.table.head2",
                    "slot.row.ga",
                    "slot.row.na",
                    "slot.row.da",
                    "slot.row.ra",
                    "slot.legend.big",
                    "slot.legend.small",
                    "slot.choice",
                ),
            ),
            Region(id="region.footer", role="footer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="87. 마을별 병원 수를 조사하여 그림그래프로 나타내었습니다.",
                style_role="question",
                x=16.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="무엇을 나타내는 그림그래프인지 알맞은 것을 선택하세요.",
                style_role="question",
                x=16.0,
                y=68.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.title",
                prompt="",
                text="마을별 병원 수",
                style_role="title",
                x=296.0,
                y=118.0,
                font_size=28,
            ),
            RectSlot(id="slot.table.outer", prompt="", x=224.0, y=150.0, width=392.0, height=270.0),
            RectSlot(id="slot.table.head1", prompt="", x=224.0, y=150.0, width=94.0, height=40.0),
            RectSlot(id="slot.table.head2", prompt="", x=318.0, y=150.0, width=298.0, height=40.0),
            TextSlot(
                id="slot.row.ga",
                prompt="",
                text="가",
                style_role="label",
                x=262.0,
                y=215.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.row.na",
                prompt="",
                text="나",
                style_role="label",
                x=262.0,
                y=272.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.row.da",
                prompt="",
                text="다",
                style_role="label",
                x=262.0,
                y=329.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.row.ra",
                prompt="",
                text="라",
                style_role="label",
                x=262.0,
                y=386.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.legend.big",
                prompt="",
                text="✚ 10개",
                style_role="label",
                x=660.0,
                y=298.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.legend.small",
                prompt="",
                text="✚ 1개",
                style_role="label",
                x=660.0,
                y=352.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 마을별 가게 수 , 마을별 병원 수 )",
                style_role="instruction",
                x=538.0,
                y=428.0,
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
    "problem_id": "S3_초등_3_008921",
    "problem_type": "그림그래프 판별",
    "metadata": {
        "language": "ko",
        "question": "마을별 병원 수를 조사하여 그림그래프로 나타내었습니다. 무엇을 나타내는 그림그래프인지 알맞은 것을 선택하세요.",
        "instruction": "무엇을 나타내는 그림그래프인지 알맞은 것을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.chart_topic", "type": "topic", "name": "마을별 병원 수"},
            {"id": "obj.legends", "type": "legend", "name": "그림기호 범례"},
            {"id": "obj.villages", "type": "category_set", "name": "가, 나, 다, 라"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.chart_topic", "obj.legends", "obj.villages"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.chart_describes", "rel.legend_supports"],
            },
            "plan": {
                "method": "chart_topic_identification",
                "description": "그림그래프의 제목과 범례, 설명 문장을 읽어 무엇을 나타내는지 확인한다.",
            },
            "execute": {"expected_operations": ["read_title", "match_description", "select_topic"]},
            "review": {"check_methods": ["title_description_consistency"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "graph_topic", "description": "무엇을 나타내는 그림그래프인지"},
        "value": "마을별 병원 수",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008921",
    "problem_type": "그림그래프 판별",
    "inputs": {
        "total_ticks": 0,
        "target_label": "그림그래프의 주제",
        "target_ticks": 0,
        "target_count": 0,
        "unit": "",
    },
    "given": [
        {"ref": "obj.chart_topic", "value": "마을별 병원 수"},
        {"ref": "obj.villages", "value": ["가", "나", "다", "라"]},
        {"ref": "obj.legends", "value": "그림기호 범례"},
    ],
    "target": {"ref": "answer.target", "type": "graph_topic"},
    "method": "chart_topic_identification",
    "plan": [
        "제목과 해설 문장을 읽어 그림그래프가 무엇을 나타내는지 확인합니다.",
        "범례와 표의 항목을 보고 주제를 고릅니다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "제목과 해설에서 나타내는 대상 읽기", "value": "마을별 병원 수"},
        {"id": "step.2", "expr": "선택해야 할 주제 확인", "value": "마을별 병원 수"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "제목과 선택 주제가 일치하는가",
            "expected": "마을별 병원 수",
            "actual": "마을별 병원 수",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "graph_topic", "description": "무엇을 나타내는 그림그래프인지"},
        "value": "마을별 병원 수",
        "unit": "",
    },
}
