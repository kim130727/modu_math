from pathlib import Path
import re

for i in range(8540, 8560):
    name = f"S3_초등_3_00{i}"
    dsl_p = Path(f"examples/problems/ko/{name}.dsl.py")
    if not dsl_p.is_file():
        continue
    c = dsl_p.read_text(encoding="utf-8")
    choice_slots = re.findall(r'(TextSlot\s*\(\s*id\s*=\s*["\']slot\.choice\.[^)]+\))', c, re.DOTALL)
    box_slots = re.findall(r'(RectSlot\s*\(\s*id\s*=\s*["\']slot\.choice\.box[^)]+\))', c, re.DOTALL)
    if choice_slots:
        print(f"=== {name} ===")
        for b in box_slots:
            print("  BOX:", " ".join(b.split()))
        for cs in choice_slots:
            print("  CHOICE:", " ".join(cs.split()))
