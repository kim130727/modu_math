from pathlib import Path

# 1. 008631
p = Path("examples/problems/ko/S3_초등_3_008631.dsl.py")
c = p.read_text(encoding="utf-8")
c = c.replace('{"id": "rel.division", "type": "division", "dividend": 69, "divisor": 3, "quotient": 23}', '{"id": "rel.division", "type": "division", "from_id": "obj.dividend", "to_id": "obj.divisor", "dividend": 69, "divisor": 3, "quotient": 23}')
c = c.replace('{"id": "rel.partition", "type": "equal_partition", "total": 69, "parts": 3, "part_value": 23}', '{"id": "rel.partition", "type": "equal_partition", "from_id": "obj.dividend", "to_id": "obj.options", "total": 69, "parts": 3, "part_value": 23}')
p.write_text(c, encoding="utf-8")

# 2. 008644
p = Path("examples/problems/ko/S3_초등_3_008644.dsl.py")
c = p.read_text(encoding="utf-8")
old_regions = '''        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=tuple(slot.id for slot in stem_slots)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=(), )),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=('slot.choice.na.copy2',))),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=tuple(slot.id for slot in answer_slots)),
        ),'''
new_regions = '''        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=tuple(slot.id for slot in stem_slots)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(slot.id for slot in diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=(*tuple(slot.id for slot in choice_slots), "slot.choice.na.copy2")),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),'''
c = c.replace(old_regions, new_regions)
p.write_text(c, encoding="utf-8")

# 3. 008647
p = Path("examples/problems/ko/S3_초등_3_008647.dsl.py")
c = p.read_text(encoding="utf-8")
c = c.replace('''            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=()
            ),
            
            ),
        ),''', '''            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=(),
            ),
        ),''')
p.write_text(c, encoding="utf-8")

# 4. 008651
p = Path("examples/problems/ko/S3_초등_3_008651.dsl.py")
c = p.read_text(encoding="utf-8")
c = c.replace('''            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
            ),
        ),''', '''            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),''')
p.write_text(c, encoding="utf-8")

# 5. 008652
p = Path("examples/problems/ko/S3_초등_3_008652.dsl.py")
c = p.read_text(encoding="utf-8")
c = c.replace('''            Region(
                id="region.characters",
                role="diagram",
                flow="absolute",
                slot_ids=(),
                    *(slot.id for slot in sunga_name),
                    *(slot.id for slot in sunga_bubble),
                    *(slot.id for slot in jaewon_character),
                    *(slot.id for slot in jaewon_name),
                    *(slot.id for slot in jaewon_bubble),
                ),
            ),''', '''            Region(
                id="region.characters",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    *(slot.id for slot in sunga_name),
                    *(slot.id for slot in sunga_bubble),
                    *(slot.id for slot in jaewon_character),
                    *(slot.id for slot in jaewon_name),
                    *(slot.id for slot in jaewon_bubble),
                ),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=(),
            ),''')
p.write_text(c, encoding="utf-8")

print("Fixed 5 files.")
