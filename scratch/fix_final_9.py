import re
from pathlib import Path

# 1. S3_초등_3_008572.dsl.py
p = Path("examples/problems/ko/S3_초등_3_008572.dsl.py")
c = p.read_text(encoding="utf-8")
c = c.replace('"objects": ["자리값을 나타내는 숫자", "곱셈 도식", "객관식 선택지"]', '''"objects": [
            {"id": "obj.place_value", "type": "concept", "name": "자리값을 나타내는 숫자"},
            {"id": "obj.mul_diagram", "type": "diagram", "name": "곱셈 도식"},
            {"id": "obj.choices", "type": "choices", "name": "객관식 선택지"},
        ]''')
c = c.replace('"choices": []', '''"choices": [
            {"id": "choice.1", "label": "①", "text": "10"},
            {"id": "choice.2", "label": "②", "text": "12"},
            {"id": "choice.3", "label": "③", "text": "100"},
            {"id": "choice.4", "label": "④", "text": "120"},
            {"id": "choice.5", "label": "⑤", "text": "1000"},
        ]''')
c = c.replace('"answer_key": []', '"answer_key": [{"id": "choice.4", "value": "120"}]')
p.write_text(c, encoding="utf-8")

# 2. S3_초등_3_008616.dsl.py
p = Path("examples/problems/ko/S3_초등_3_008616.dsl.py")
c = p.read_text(encoding="utf-8")
c = c.replace('''        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.text", "slot.eq.box", "slot.eq.text"),                 
                ),
            ),
        ),''', '''        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.text", "slot.eq.box", "slot.eq.text"),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=(),
            ),
        ),''')
p.write_text(c, encoding="utf-8")

# 3. S3_초등_3_008631.dsl.py
p = Path("examples/problems/ko/S3_초등_3_008631.dsl.py")
c = p.read_text(encoding="utf-8")
c = c.replace('''        "relations": [
            {"id": "rel.division", "type": "division_operation", "operation": "69 / 3 = 23"},
            {"id": "rel.partition", "type": "equal_partition", "total": 69, "parts": 3, "part_value": 23},
        ],''', '''        "relations": [
            {"id": "rel.division", "type": "division_operation", "from_id": "obj.dividend", "to_id": "obj.divisor", "operation": "69 / 3 = 23"},
            {"id": "rel.partition", "type": "equal_partition", "from_id": "obj.dividend", "to_id": "obj.options", "total": 69, "parts": 3, "part_value": 23},
        ],''')
c = c.replace('"choices": []', '''"choices": [
            {"id": "choice.1", "label": "①", "text": "21"},
            {"id": "choice.2", "label": "②", "text": "22"},
            {"id": "choice.3", "label": "③", "text": "23"},
            {"id": "choice.4", "label": "④", "text": "24"},
            {"id": "choice.5", "label": "⑤", "text": "25"},
        ]''')
c = c.replace('"answer_key": []', '"answer_key": [{"id": "choice.3", "value": "23"}]')
p.write_text(c, encoding="utf-8")

# 4. S3_초등_3_008644.dsl.py
p = Path("examples/problems/ko/S3_초등_3_008644.dsl.py")
c = p.read_text(encoding="utf-8")
c = re.sub(r'regions=\([^)]+\),', '''regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=tuple(slot.id for slot in stem_slots)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(slot.id for slot in diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=tuple(slot.id for slot in choice_slots)),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),''', c)
p.write_text(c, encoding="utf-8")

# 5. S3_초등_3_008647.dsl.py
p = Path("examples/problems/ko/S3_초등_3_008647.dsl.py")
c = p.read_text(encoding="utf-8")
c = re.sub(r'Region\(\s*id="region\.explanation"[^)]+\),', '', c)
p.write_text(c, encoding="utf-8")

# 6. S3_초등_3_008651.dsl.py
p = Path("examples/problems/ko/S3_초등_3_008651.dsl.py")
c = p.read_text(encoding="utf-8")
c = re.sub(r'Region\(\s*id="region\.answer"[^)]+\)', 'Region(id="region.answer", role="answer", flow="absolute", slot_ids=())', c)
p.write_text(c, encoding="utf-8")

# 7. S3_초등_3_008652.dsl.py
p = Path("examples/problems/ko/S3_초등_3_008652.dsl.py")
c = p.read_text(encoding="utf-8")
c = re.sub(r'Region\(\s*id="region\.answer"[^)]+\)', 'Region(id="region.answer", role="answer", flow="absolute", slot_ids=())', c)
c = re.sub(r'slot_ids\s*=\s*\(\s*\)\s*\)\s*,', 'slot_ids=(),', c)
p.write_text(c, encoding="utf-8")

# 8. S3_초등_3_008709.dsl.py
p = Path("examples/problems/ko/S3_초등_3_008709.dsl.py")
c = p.read_text(encoding="utf-8")
c = c.replace('"answer_key": [3]', '"answer_key": [{"id": "choice.3", "value": "ㅁㅂ"}]')
c = re.sub(r'"choices"\s*:\s*\[[^\]]+\]', '''"choices": [
            {"id": "choice.1", "label": "①", "text": "ㄱㄴ"},
            {"id": "choice.2", "label": "②", "text": "ㄷㄹ"},
            {"id": "choice.3", "label": "③", "text": "ㅁㅂ"},
            {"id": "choice.4", "label": "④", "text": "ㅅㅈ"},
        ]''', c)
p.write_text(c, encoding="utf-8")

# 9. S3_초등_3_008798.dsl.py
p = Path("examples/problems/ko/S3_초등_3_008798.dsl.py")
c = p.read_text(encoding="utf-8")
c = c.replace('slot_ids="slot.body"', 'slot_ids=("slot.body",)')
c = c.replace("slot_ids='slot.body'", "slot_ids=('slot.body',)")
p.write_text(c, encoding="utf-8")

print("Fixed final 9 files.")
