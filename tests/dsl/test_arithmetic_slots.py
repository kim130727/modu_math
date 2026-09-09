from __future__ import annotations

import pytest

from modu_math.dsl import columnar_number_slots


def test_columnar_number_slots_use_fixed_right_aligned_columns() -> None:
    slots = columnar_number_slots(
        id_prefix="slot.multiply.partial",
        value="3200",
        right_x=295,
        y=288,
        column_width=34,
    )

    assert [slot.id for slot in slots] == [
        "slot.multiply.partial.place.3",
        "slot.multiply.partial.place.2",
        "slot.multiply.partial.place.1",
        "slot.multiply.partial.place.0",
    ]
    assert [slot.text for slot in slots] == ["3", "2", "0", "0"]
    assert [slot.x for slot in slots] == [193, 227, 261, 295]
    assert all(slot.anchor == "middle" for slot in slots)
    assert all(" " not in slot.text for slot in slots)


@pytest.mark.parametrize("value", ["", "3 200", "3.2", "-4"])
def test_columnar_number_slots_reject_spacing_and_non_digits(value: str) -> None:
    with pytest.raises(ValueError):
        columnar_number_slots(
            id_prefix="slot.row",
            value=value,
            right_x=100,
            y=100,
            column_width=30,
        )
