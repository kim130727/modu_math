from manim import *
import json


class TimeConversionProblem(Scene):
    def construct(self):
        # 1) JSON 데이터(코드에 직접 임베드)
        problem_json = r"""
        {
          "id": 1,
          "type": "fill_in_blank",
          "category": "time_conversion",
          "instruction": "□안에 알맞은 수를 구하시오.",
          "question": {
            "left_seconds": 410,
            "minutes": 6,
            "blank_symbol": "□",
            "unit_from": "초",
            "unit_mid": "분",
            "unit_to": "초"
          },
          "answer": 50
        }
        """
        data = json.loads(problem_json)

        # 2) 배경
        self.camera.background_color = "#F6F6F6"

        # 3) 상단 지시문
        instruction_text = Text(
            data["instruction"],
            font="Malgun Gothic",
            font_size=28,
            color=BLACK,
        )
        instruction_text.to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.4)

        # 4) 문제 박스
        box = RoundedRectangle(
            corner_radius=0.25,
            width=7.5,
            height=2.0,
            stroke_color=BLACK,
            stroke_width=1.5,
            fill_opacity=0,
        )
        box.move_to(ORIGIN + DOWN * 0.1)

        q = data["question"]
        expr = (
            f'{q["left_seconds"]}{q["unit_from"]}='
            f'{q["minutes"]}{q["unit_mid"]} '
            f'{q["blank_symbol"]}{q["unit_to"]}'
        )
        expr_text = Text(
            expr,
            font="Malgun Gothic",
            font_size=34,
            color=BLACK,
        )
        expr_text.move_to(box.get_center())

        # 5) 아래 괄호(정답 작성 칸)
        left_paren = Text("(", font="Malgun Gothic", font_size=34, color=BLACK)
        right_paren = Text(")", font="Malgun Gothic", font_size=34, color=BLACK)
        left_paren.move_to(DOWN * 2.2 + RIGHT * 1.5)
        right_paren.move_to(DOWN * 2.2 + RIGHT * 4.9)

        # 6) 화면 표시
        self.add(instruction_text, box, expr_text, left_paren, right_paren)

        # 필요 시 정답 표시(주석 해제)
        # answer_text = Text(
        #     f'정답: {data["answer"]}',
        #     font="Malgun Gothic",
        #     font_size=24,
        #     color=BLUE,
        # )
        # answer_text.next_to(box, DOWN, buff=1.0)
        # self.add(answer_text)

        self.wait(2)

