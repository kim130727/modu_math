from manim import *
import json

class RulerEraserProblem(Scene):
    def construct(self):
        # -----------------------------
        # 1) JSON 데이터
        # -----------------------------
        problem_json = r"""
        {
          "id": 2,
          "type": "measure_length_with_ruler",
          "instruction": "2. 지우개의 길이는 몇 mm입니까?",
          "sub_instruction": "(* 눈금을 잘 보아야해요)",
          "object_label": "지우개",
          "ruler": {
            "start_cm": 2,
            "end_cm": 5,
            "major_ticks": [2, 3, 4, 5],
            "minor_per_cm": 10
          },
          "measurement": {
            "left_cm": 3.0,
            "right_cm": 4.6
          },
          "answer_mm": 16
        }
        """
        data = json.loads(problem_json)

        self.camera.background_color = "#f7f7f7"

        # -----------------------------
        # 2) 상단 문제 문장
        # -----------------------------
        title = Text(
            data["instruction"],
            font="Malgun Gothic",
            font_size=30,
            color=BLACK
        )
        title.to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.3)

        subtitle = Text(
            data["sub_instruction"],
            font="Malgun Gothic",
            font_size=22,
            color=BLACK
        )
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.22)

        # -----------------------------
        # 3) 자 설정
        # -----------------------------
        ruler_left = LEFT * 4.6 + DOWN * 1.2
        ruler_width = 8.4
        ruler_height = 1.8

        ruler_rect = Rectangle(
            width=ruler_width,
            height=ruler_height,
            stroke_color="#C9A000",
            stroke_width=6,
            fill_opacity=0
        )
        ruler_rect.move_to(ruler_left + RIGHT * (ruler_width / 2) + DOWN * 0.1)

        # 눈금 범위
        start_cm = data["ruler"]["start_cm"]
        end_cm = data["ruler"]["end_cm"]
        total_cm = end_cm - start_cm
        minor_per_cm = data["ruler"]["minor_per_cm"]

        # 자 윗변 기준선
        ruler_top_y = ruler_rect.get_top()[1]
        ruler_bottom_y = ruler_rect.get_bottom()[1]

        # 숫자와 눈금 그룹
        tick_group = VGroup()
        number_group = VGroup()

        def x_from_cm(cm_value: float):
            ratio = (cm_value - start_cm) / total_cm
            return ruler_rect.get_left()[0] + ratio * ruler_width

        # 1mm 단위 눈금
        total_minor_steps = total_cm * minor_per_cm
        for i in range(total_minor_steps + 1):
            cm_value = start_cm + i / minor_per_cm
            x = x_from_cm(cm_value)

            # 정수 cm 여부
            if abs(cm_value - round(cm_value)) < 1e-8:
                tick_len = 0.7
                stroke_w = 6
            else:
                tick_len = 0.35
                stroke_w = 5

            tick = Line(
                start=[x, ruler_top_y, 0],
                end=[x, ruler_top_y - tick_len, 0],
                color="#C9A000",
                stroke_width=stroke_w
            )
            tick_group.add(tick)

        # 숫자 2,3,4,5
        for major in data["ruler"]["major_ticks"]:
            x = x_from_cm(major)
            num = Text(
                str(major),
                font="Arial",
                font_size=30,
                color=BLACK
            )
            num.move_to([x, ruler_bottom_y + 0.45, 0])
            number_group.add(num)

        # -----------------------------
        # 4) 지우개 위치
        # -----------------------------
        left_cm = data["measurement"]["left_cm"]
        right_cm = data["measurement"]["right_cm"]

        left_x = x_from_cm(left_cm)
        right_x = x_from_cm(right_cm)
        eraser_center_x = (left_x + right_x) / 2

        eraser_width = right_x - left_x
        eraser_height = 1.4

        eraser = RoundedRectangle(
            corner_radius=0.22,
            width=eraser_width,
            height=eraser_height,
            stroke_color="#4F6FB3",
            stroke_width=1.5,
            fill_color="#D9E5CF",
            fill_opacity=1.0
        )
        eraser.move_to([eraser_center_x, ruler_top_y + 0.75, 0])

        eraser_label = Text(
            data["object_label"],
            font="Malgun Gothic",
            font_size=34,
            color=BLACK,
            weight=BOLD
        )
        eraser_label.move_to(eraser.get_center())

        # -----------------------------
        # 5) 점선 가이드
        # -----------------------------
        dash_top_y = eraser.get_top()[1] + 0.35
        dash_bottom_y = ruler_top_y - 0.05

        left_dash = DashedLine(
            start=[left_x, dash_top_y, 0],
            end=[left_x, dash_bottom_y, 0],
            color=BLACK,
            dash_length=0.12,
            stroke_width=3
        )
        right_dash = DashedLine(
            start=[right_x, dash_top_y, 0],
            end=[right_x, dash_bottom_y, 0],
            color=BLACK,
            dash_length=0.12,
            stroke_width=3
        )

        # -----------------------------
        # 6) 아래 답칸 괄호
        # -----------------------------
        left_paren = Text(
            "(",
            font="Arial",
            font_size=30,
            color=BLACK
        )
        right_paren = Text(
            ")",
            font="Arial",
            font_size=30,
            color=BLACK
        )

        left_paren.move_to([0.4, -3.05, 0])
        right_paren.move_to([4.4, -3.05, 0])

        # -----------------------------
        # 7) 장면 추가
        # -----------------------------
        self.add(
            title,
            subtitle,
            ruler_rect,
            tick_group,
            number_group,
            eraser,
            eraser_label,
            left_dash,
            right_dash,
            left_paren,
            right_paren
        )

        self.wait(2)