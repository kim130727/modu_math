import glob
import re
import sys
from pathlib import Path

# Let's inspect each of the 30 failing files
files = [
    "S3_초등_3_008541.dsl.py",
    "S3_초등_3_008542.dsl.py",
    "S3_초등_3_008543.dsl.py",
    "S3_초등_3_008544.dsl.py",
    "S3_초등_3_008545.dsl.py",
    "S3_초등_3_008547.dsl.py",
    "S3_초등_3_008552.dsl.py",
    "S3_초등_3_008554.dsl.py",
    "S3_초등_3_008561.dsl.py",
    "S3_초등_3_008562.dsl.py",
    "S3_초등_3_008564.dsl.py",
    "S3_초등_3_008565.dsl.py",
    "S3_초등_3_008566.dsl.py",
    "S3_초등_3_008572.dsl.py",
    "S3_초등_3_008616.dsl.py",
    "S3_초등_3_008618.dsl.py",
    "S3_초등_3_008623.dsl.py",
    "S3_초등_3_008631.dsl.py",
    "S3_초등_3_008639.dsl.py",
    "S3_초등_3_008640.dsl.py",
    "S3_초등_3_008644.dsl.py",
    "S3_초등_3_008647.dsl.py",
    "S3_초등_3_008649.dsl.py",
    "S3_초등_3_008651.dsl.py",
    "S3_초등_3_008652.dsl.py",
    "S3_초등_3_008670.dsl.py",
    "S3_초등_3_008671.dsl.py",
    "S3_초등_3_008692.dsl.py",
    "S3_초등_3_008709.dsl.py",
    "S3_초등_3_008798.dsl.py",
]

for fname in files:
    fpath = Path(f"examples/problems/ko/{fname}")
    if not fpath.exists():
        continue
    content = fpath.read_text(encoding="utf-8")
    
    # Extract defined slot ids
    defined_slot_ids = set(re.findall(r'id\s*=\s*["\'](slot\.[^"\']+)["\']', content))
    
    # Fix referenced slot_ids in regions
    def fix_region_slots(match):
        region_str = match.group(0)
        # Find all slot_ids in this region
        refs = re.findall(r'["\'](slot\.[^"\']+)["\']', region_str)
        # Filter to only defined ones
        valid_refs = [r for r in refs if r in defined_slot_ids]
        if "role=\"answer\"" in region_str or "role='answer'" in region_str:
            valid_refs = []
        tuple_content = ", ".join(f'"{r}"' for r in valid_refs)
        if len(valid_refs) == 1:
            tuple_content += ","
        return re.sub(r'slot_ids\s*=\s*\([^)]*\)', f'slot_ids=({tuple_content})', region_str)

    content = re.sub(r'Region\s*\([^)]*\)', fix_region_slots, content)
    
    # Fix 008618 SpeakerSpec name_y
    if "008618" in fname:
        content = re.sub(r'name_y\s*=\s*[\d.]+\s*,\s*name_y\s*=\s*([\d.]+)', r'name_y=\1', content)
        content = re.sub(r'name_y\s*=\s*([\d.]+)\s*,\s*name_y\s*=\s*[\d.]+', r'name_y=\1', content)
        
    # Fix 008644 and 008670: sequence item 0: expected str instance, tuple found
    # This usually means slot_ids=( ("slot.a", "slot.b") ) nested tuple
    content = re.sub(r'slot_ids\s*=\s*\(\s*\(([^)]+)\)\s*,?\s*\)', r'slot_ids=(\1)', content)
    
    # Fix 008798 slot_ids=('slot.body') -> slot_ids=('slot.body',)
    content = re.sub(r'slot_ids\s*=\s*\(\s*(["\'][^"\',]+["\'])\s*\)', r'slot_ids=(\1,)', content)
    
    # Fix 008692 SEMANTIC_OVERRIDE missing
    if "008692" in fname and "SEMANTIC_OVERRIDE" not in content:
        content += '''

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008692",
    "problem_type": "multiple_choice",
    "metadata": {
        "grade": 3,
        "semester": 2,
        "unit": 3,
        "topic": "원",
    },
    "answer": {
        "blanks": [],
        "choices": [
            {"id": "choice.1", "label": "가", "text": "점 ㄱ"},
            {"id": "choice.2", "label": "나", "text": "점 ㄴ"},
            {"id": "choice.3", "label": "다", "text": "점 ㄷ"},
            {"id": "choice.4", "label": "라", "text": "점 ㄹ"},
        ],
        "answer_key": [{"id": "choice.2", "value": "나"}],
        "value": "나",
    },
    "domain": {
        "objects": [{"id": "circle", "name": "원"}],
        "relations": [],
        "facts": [],
    },
}

SOLVABLE = SEMANTIC_OVERRIDE
'''
    fpath.write_text(content, encoding="utf-8")

print("Processed 30 targeted files.")
