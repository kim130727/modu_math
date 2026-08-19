import glob
import json
import subprocess
from pathlib import Path

files = sorted(glob.glob("examples/problems/ko/S3_초등_3_*.dsl.py"))

missing_answer_region = []
has_blank_slot_files = []

for f in files:
    content = Path(f).read_text(encoding="utf-8")
    if 'role="answer"' not in content and "role='answer'" not in content:
        missing_answer_region.append(f)
    if "BlankSlot" in content:
        has_blank_slot_files.append(f)

print(f"Missing answer region: {len(missing_answer_region)}")
print(f"Has BlankSlot: {len(has_blank_slot_files)}")
if has_blank_slot_files:
    print(f"Files with BlankSlot: {has_blank_slot_files}")
print("First 10 missing answer region:")
for f in missing_answer_region[:10]:
    print(f"  {f}")
