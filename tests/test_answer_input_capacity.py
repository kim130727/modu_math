from copy import deepcopy

import pytest
from modu_math.dsl.compiler_to_layout import _normalize_answer_input_interaction as normalize_slot
from modu_math.layout.editor_overrides import _normalize_answer_input_interaction as normalize_override


@pytest.mark.parametrize("width", [30, 60, 240])
def test_resizing_digit_cells_does_not_change_input_semantics(width):
    interaction = {
        "type": "input", "role": "answer", "value_type": "digit",
        "max_length": 1, "auto_advance": True,
    }
    content = {"width": width, "interaction": deepcopy(interaction)}
    normalize_slot({"content": content})
    assert {key: content["interaction"][key] for key in interaction} == interaction
    normalize_override(content)
    assert {key: content["interaction"][key] for key in interaction} == interaction
