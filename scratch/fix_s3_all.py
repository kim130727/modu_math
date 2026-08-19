import glob
import re
import sys
import importlib.util
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "tools")
from validate_generated_dsl import _load_module, _run_build, _default_out_prefix

files = sorted(glob.glob("examples/problems/ko/S3_초등_3_*.dsl.py"))

def fix_s3_code(content: str, file_path: Path) -> str:
    # 1. Fix single string tuple bug in regions: slot_ids=("...") -> slot_ids=("...",)
    content = re.sub(
        r'slot_ids\s*=\s*\(\s*(["\'][^"\',]+["\'])\s*\)',
        r'slot_ids=(\1,)',
        content
    )
    
    # 2. Fix SpeakerSpec multiple name_y
    content = re.sub(r'name_y\s*=\s*[\d.]+\s*,\s*name_y\s*=\s*([\d.]+)', r'name_y=\1', content)

    # 3. Fix 008577 ProblemTemplate.id
    if file_path.name == "S3_초등_3_008577.dsl.py":
        content = content.replace('"S3_초등_3_008576"', '"S3_초등_3_008577"')

    # 4. Fix choices list of strings: ["ㄱ", "ㄴ", "ㄷ"] -> [{"id": "choice.1", "label": "ㄱ", "text": "ㄱ"}, ...]
    # Handle simple list of strings in answer choices
    def replace_choices(match):
        block = match.group(0)
        # find string items
        items = re.findall(r'["\']([^"\']+)["\']', block)
        if items and not any("{" in it for it in items):
            # Check if all items are simple strings
            obj_strs = [f'{{"id": "choice.{i+1}", "label": "{it}", "text": "{it}"}}' for i, it in enumerate(items)]
            return '"choices": [\n            ' + ',\n            '.join(obj_strs) + '\n        ]'
        return block

    content = re.sub(r'"choices"\s*:\s*\[\s*(["\'][^"\'\{\}]+["\']\s*,\s*)*["\'][^"\'\{\}]+["\']\s*\]', replace_choices, content)

    return content

for f in files:
    path = Path(f)
    old = path.read_text(encoding="utf-8")
    new = fix_s3_code(old, path)
    if new != old:
        path.write_text(new, encoding="utf-8")

print("Basic string/tuple fixes applied.")
