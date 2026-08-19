from pathlib import Path
import json

for i in range(8540, 8560):
    name = f"S3_초등_3_00{i}"
    dsl_p = Path(f"examples/problems/ko/{name}.dsl.py")
    ov_p = Path(f"examples/problems/ko/{name}.editor_overrides.json")
    if not dsl_p.is_file():
        continue
    c = dsl_p.read_text(encoding="utf-8")
    has_choices = "slot.choice" in c
    print(f"=== {name} (has_choices: {has_choices}, has_override: {ov_p.is_file()}) ===")
    if ov_p.is_file():
        ov = json.loads(ov_p.read_text(encoding="utf-8"))
        for k, v in ov.get("slots", {}).items():
            if "choice" in k:
                print(f"  OV {k}: {v}")
