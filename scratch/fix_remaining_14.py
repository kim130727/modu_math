import re
from pathlib import Path

# 1. Fix 008545 choices
p = Path("examples/problems/ko/S3_초등_3_008545.dsl.py")
c = p.read_text(encoding="utf-8")
c = c.replace('"choices": [\n            "412 × 4",\n            "526 × 3",\n        ]', '''"choices": [
            {"id": "choice.1", "label": "①", "text": "412 × 4"},
            {"id": "choice.2", "label": "②", "text": "526 × 3"},
        ]''')
c = c.replace('"choices": [\n            "412 x 4",\n            "526 x 3",\n        ]', '''"choices": [
            {"id": "choice.1", "label": "①", "text": "412 × 4"},
            {"id": "choice.2", "label": "②", "text": "526 × 3"},
        ]''')
p.write_text(c, encoding="utf-8")

# 2. Fix 008564
p = Path("examples/problems/ko/S3_초등_3_008564.dsl.py")
c = p.read_text(encoding="utf-8")
c = c.replace('slot_ids=("slot.box",),', 'slot_ids=(\n                    "slot.box",')
p.write_text(c, encoding="utf-8")

# 3. Fix 008572
p = Path("examples/problems/ko/S3_초등_3_008572.dsl.py")
c = p.read_text(encoding="utf-8")
c = c.replace('"objects": ["obj.1", "obj.2"]', '"objects": [{"id": "obj.1", "type": "number", "name": "obj.1"}, {"id": "obj.2", "type": "number", "name": "obj.2"}]')
c = c.replace('"objects": [{"id": "obj.1"}, {"id": "obj.2"}]', '"objects": [{"id": "obj.1", "type": "number", "name": "obj.1"}, {"id": "obj.2", "type": "number", "name": "obj.2"}]')
# if objects has string items
c = re.sub(r'"objects"\s*:\s*\[\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\]', r'"objects": [{"id": "\1", "type": "number", "name": "\1"}, {"id": "\2", "type": "number", "name": "\2"}]', c)
p.write_text(c, encoding="utf-8")

# 4. Fix 008616
p = Path("examples/problems/ko/S3_초등_3_008616.dsl.py")
c = p.read_text(encoding="utf-8")
c = re.sub(r'(\n\s*)(\n\s+TextSlot\(id="slot\.q\.text")', r'\1TextSlot(id="slot.q.text"', c)
p.write_text(c, encoding="utf-8")

# 5. Fix 008618
p = Path("examples/problems/ko/S3_초등_3_008618.dsl.py")
c = p.read_text(encoding="utf-8")
c = re.sub(r'SpeakerSpec\([^)]*\)', lambda m: re.sub(r'name_y\s*=\s*[\d.]+\s*,\s*', '', m.group(0), count=1), c)
p.write_text(c, encoding="utf-8")

# 6. Fix 008631
p = Path("examples/problems/ko/S3_초등_3_008631.dsl.py")
c = p.read_text(encoding="utf-8")
c = c.replace('"from": ""', '"from_id": "choice.1"')
c = c.replace('"to": ""', '"to_id": "answer"')
c = c.replace('"from_id": ""', '"from_id": "choice.1"')
c = c.replace('"to_id": ""', '"to_id": "answer"')
p.write_text(c, encoding="utf-8")

# 7. Fix 008644
p = Path("examples/problems/ko/S3_초등_3_008644.dsl.py")
c = p.read_text(encoding="utf-8")
c = c.replace("slot_ids=(), 'slot.choice.na.copy2'", "slot_ids=('slot.choice.na.copy2',)")
p.write_text(c, encoding="utf-8")

# 8. Fix 008647
p = Path("examples/problems/ko/S3_초등_3_008647.dsl.py")
c = p.read_text(encoding="utf-8")
c = c.replace('slot_ids=(),\n                    "slot.explanation.text1",\n                    "slot.explanation.text2",', 'slot_ids=(\n                    "slot.explanation.text1",\n                    "slot.explanation.text2",')
c = c.replace('slot_ids=(),', 'slot_ids=()')
p.write_text(c, encoding="utf-8")

# 9. Fix 008651
p = Path("examples/problems/ko/S3_초등_3_008651.dsl.py")
c = p.read_text(encoding="utf-8")
c = re.sub(r'slot_ids\s*=\s*\(\s*\)\s*,\s*(["\'][^"\']+["\'])', r'slot_ids=(\1', c)
p.write_text(c, encoding="utf-8")

# 10. Fix 008652
p = Path("examples/problems/ko/S3_초등_3_008652.dsl.py")
c = p.read_text(encoding="utf-8")
c = re.sub(r'slot_ids\s*=\s*\(\s*\)\s*,\s*(["\'][^"\']+["\'])', r'slot_ids=(\1', c)
p.write_text(c, encoding="utf-8")

# 11. Fix 008709
p = Path("examples/problems/ko/S3_초등_3_008709.dsl.py")
c = p.read_text(encoding="utf-8")
c = re.sub(r'"blanks"\s*:\s*\[[^\]]*\]', '"blanks": []', c)
p.write_text(c, encoding="utf-8")

# 12. Fix 008798
p = Path("examples/problems/ko/S3_초등_3_008798.dsl.py")
c = p.read_text(encoding="utf-8")
c = c.replace('slot_ids=("slot.body")', 'slot_ids=("slot.body",)')
c = c.replace("slot_ids=('slot.body')", "slot_ids=('slot.body',)")
c = c.replace('slot_ids = ("slot.body")', 'slot_ids = ("slot.body",)')
p.write_text(c, encoding="utf-8")

print("Fixes applied.")
