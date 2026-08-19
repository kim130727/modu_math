from pathlib import Path
import re

problems = list(Path("examples/problems/ko").glob("S3_초등_3_*.dsl.py"))
print(f"Total S3 problems: {len(problems)}")

choice_box_problems = []
for p in problems:
    c = p.read_text(encoding="utf-8")
    if "choice.box" in c or "choice.1" in c:
        choice_box_problems.append(p.name)

print(f"Problems with choices in DSL: {len(choice_box_problems)}")
print(choice_box_problems[:20])
