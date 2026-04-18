import json
from pathlib import Path
import os
import shutil

root = Path(r"C:\projects\modu_math\sample_data\problems\ke_3rd")

# Mapping from problem_type or path to broad category
# I'll use the topic from metadata if available, else infer.
category_map = {
    "Addition and Subtraction": "덧셈과_뺄셈",
    "2D Shapes": "평면도형",
    "Length and Time": "길이와_시간",
    "addition_subtraction": "덧셈과_뺄셈",
    "shape2d": "평면도형"
}

problems = []

for problem_dir in root.iterdir():
    if not problem_dir.is_dir():
        continue
    
    # Skip if it's already a category folder (we'll check later)
    if problem_dir.name in category_map.values():
        continue

    # Find semantic.json
    semantic_files = list(problem_dir.glob("*.semantic.json"))
    if not semantic_files:
        continue
        
    semantic_path = semantic_files[0]
    with open(semantic_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 1. Get Category
    category = "기타"
    topic = data.get("metadata", {}).get("classification", {}).get("topic")
    if topic and topic in category_map:
        category = category_map[topic]
    elif "addition_subtraction" in problem_dir.name:
        category = "덧셈과_뺄셈"
    elif "shape2d" in problem_dir.name:
        category = "평면도형"
    elif "000" in problem_dir.name:
        # Fallback for 0001-0010 if topic missing (should be enriched though)
        num = int(problem_dir.name)
        if 1 <= num <= 9: category = "덧셈과_뺄셈"
        elif num == 10: category = "길이와_시간"
    
    # 2. Get Descriptive Name
    title = data.get("title", problem_dir.name)
    # Sanitize title for filename
    safe_title = "".join([c if c.isalnum() or c in " _-" else "_" for c in title]).strip()
    # Problem ID for uniqueness
    prob_id = data.get("problem_id", problem_dir.name)
    new_dir_name = f"{prob_id}_{safe_title}"
    
    problems.append({
        "old_path": problem_dir,
        "category": category,
        "new_name": new_dir_name
    })

# Execute move
for p in problems:
    cat_dir = root / p["category"]
    cat_dir.mkdir(exist_ok=True)
    
    dst = cat_dir / p["new_name"]
    print(f"Moving {p['old_path'].name} -> {p['category']}/{p['new_name']}")
    
    # Handle collisions
    if dst.exists():
        print(f"  Warning: {dst} already exists. Skipping or merging.")
        # We'll merge by moving files if needed, but for now just skip to be safe
    else:
        shutil.move(str(p["old_path"]), str(dst))

print("Classification and renaming complete.")
