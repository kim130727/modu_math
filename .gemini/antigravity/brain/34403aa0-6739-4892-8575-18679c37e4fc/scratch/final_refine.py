import json
import os
import shutil
import re
from pathlib import Path

root = Path(r"C:\projects\modu_math\sample_data\problems\ke_3rd")

category_folders = [
    "1. 길이와 시간",
    "2. 덧셈과 뺄셈",
    "3. 평면도형"
]

for cat_name in category_folders:
    cat_dir = root / cat_name
    if not cat_dir.exists():
        continue
    
    for problem_dir in list(cat_dir.iterdir()):
        if not problem_dir.is_dir():
            continue
        
        # Find semantic.json
        semantic_files = list(problem_dir.glob("*.semantic.json"))
        if not semantic_files:
            continue
        
        with open(semantic_files[0], "r", encoding="utf-8") as f:
            data = json.load(f)
        
        prob_id = data.get("problem_id", "")
        title = data.get("title", "")
        
        # Extract the last 4 digits of prob_id as number
        num_match = re.search(r"(\d{4})$", prob_id)
        num = num_match.group(1) if num_match else "0000"
        
        # Sanitize title
        safe_title = "".join([c if c.isalnum() or c in " _-" else "_" for c in title]).strip()
        
        new_name = f"{num}_{safe_title}"
        dst = cat_dir / new_name
        
        if dst != problem_dir:
            print(f"Renaming {problem_dir.name} -> {new_name}")
            if dst.exists():
                # If collision, add problem_id prefix to be unique but clean
                # or just add a suffix
                new_name = f"{num}_{safe_title}_{prob_id}"
                dst = cat_dir / new_name
                print(f"  Collision! Using {new_name} instead.")
            
            shutil.move(str(problem_dir), str(dst))

print("Final refinement complete.")
