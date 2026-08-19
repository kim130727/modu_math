import glob
import re
import ast
import json
from pathlib import Path

files = sorted(glob.glob("examples/problems/ko/S3_초등_3_*.dsl.py"))

def fix_file(file_path: str) -> bool:
    path = Path(file_path)
    content = path.read_text(encoding="utf-8")
    original = content
    
    # 1. Fix single-string tuple bug: slot_ids=("slot.something") -> slot_ids=("slot.something",)
    # or slot_ids = ('slot.something') -> slot_ids = ('slot.something',)
    content = re.sub(
        r'slot_ids\s*=\s*\(\s*(["\'][^"\',]+["\'])\s*\)',
        r'slot_ids=(\1,)',
        content
    )
    
    # 2. Fix SpeakerSpec multiple values for name_y
    if "name_y=" in content and "SpeakerSpec(" in content:
        # Check if name_y is duplicated
        content = re.sub(r'name_y\s*=\s*[\d.]+\s*,\s*name_y\s*=\s*([\d.]+)', r'name_y=\1', content)

    # 3. Write back if modified
    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False

modified_count = 0
for f in files:
    if fix_file(f):
        modified_count += 1

print(f"Fixed single-string tuples in {modified_count} files.")
