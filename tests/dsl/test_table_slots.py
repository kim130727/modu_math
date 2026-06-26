from modu_math.dsl import TextSlot, table_slots


def test_table_slots_center_text_by_default() -> None:
    slots = table_slots(
        "slot.table",
        x=10,
        y=20,
        col_widths=(100, 80),
        row_heights=(40, 50),
        cells=(("A", "B"), ("C", "D")),
        font_size=20,
    )

    text_slots = [slot for slot in slots if isinstance(slot, TextSlot)]

    assert text_slots[0].anchor == "middle"
    assert text_slots[0].x == 60
    assert text_slots[0].y == 47
    assert text_slots[1].x == 150
    assert text_slots[2].y == 20 + 40 + 25 + 7
