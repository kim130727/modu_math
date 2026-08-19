from pathlib import Path
import json
import re

problems = sorted(list(Path("examples/problems/ko").glob("S3_초등_3_*.dsl.py")))

for p in problems:
    override_file = p.with_name(p.stem.replace(".dsl", "") + ".editor_overrides.json")
    # check dsl text for choices
    txt = p.read_text(encoding="utf-8")
    if "slot.choice.1" in txt and "slot.choice.4" in txt:
        print(f"=== {p.name} ===")
        # extract choice coordinates in dsl
        for match in re.finditer(r'id=["\'](slot\.choice\.[1-4]|slot\.choice\.box)["\'].*?x\s*=\s*([0-9.]+).*?y\s*=\s*([0-9.]+)', txt, re.DOTALL):
            print(f"  DSL: {match.group(1)} -> x={match.group(2)}, y={match.group(3)}")
        if override_file.is_file():
            ov = json.loads(override_file.read_text(encoding="utf-8"))
            slots = ov.get("slots", {})
            for k in ["slot.choice.box", "slot.choice.1", "slot.choice.2", "slot.choice.3", "slot.choice.4"]:
                if k in slots:
                    print(f"  OVERRIDE: {k} -> {slots[k]}")
