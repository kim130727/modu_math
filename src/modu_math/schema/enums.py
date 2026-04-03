from __future__ import annotations

from enum import StrEnum


class SemanticRole(StrEnum):
    INSTRUCTION = "instruction"
    SUB_INSTRUCTION = "sub_instruction"
    EQUATION = "equation"
    ANSWER_BLANK = "answer_blank"
    CHOICE_OPTION = "choice_option"
    SCALE = "scale"
    TICK_MAJOR = "tick_major"
    TICK_MINOR = "tick_minor"
    MEASUREMENT_GUIDE = "measurement_guide"


class FigureType(StrEnum):
    BLANK_BOX = "blank_box"
    ROUNDED_BOX = "rounded_box"
    RULER = "ruler"
    SCALE_TICK = "scale_tick"
    ONE_CUBE = "one_cube"
    TEN_CUBES = "ten_cubes"
    HUNDRED_CUBES = "hundred_cubes"
