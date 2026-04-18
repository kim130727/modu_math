import json
from pathlib import Path
import os
import shutil
import re

root = Path(r"C:\projects\modu_math\sample_data\problems\ke_3rd")

# Mapping from categories to numbers
category_folders = {
    "덧셈과_뺄셈": "2. 덧셈과 뺄셈",
    "평면도형": "3. 평면도형",
    "길이와_시간": "1. 길이와 시간"
}

# Iterate through the existing category folders
for cat_key, cat_folder_name in category_folders.items():
    old_cat_dir = root / cat_key
    new_cat_dir = root / cat_folder_name
    
    if old_cat_dir.exists():
        if not new_cat_dir.exists():
            shutil.move(str(old_cat_dir), str(new_cat_dir))
        else:
            # Merge if both exist
            for p_dir in old_cat_dir.iterdir():
                if p_dir.is_dir():
                    shutil.move(str(p_dir), str(new_cat_dir / p_dir.name))
            shutil.rmtree(old_cat_dir)

# Now iterate through the new category folders and rename problem folders
for cat_folder_name in category_folders.values():
    cat_dir = root / cat_folder_name
    if not cat_dir.exists():
        continue
    
    for problem_dir in cat_dir.iterdir():
        if not problem_dir.is_dir():
            continue
        
        # Current name example: ke_3rd_0001_바둑돌_빼기
        # We want: 0001_바둑돌_빼기
        
        name = problem_dir.name
        # Regex to match [prefix]_[number]_[title]
        # or [number]_[title]
        match = re.search(r"(\d{4})_(.*)", name)
        if match:
            num = match.group(1)
            title = match.group(2)
            new_name = f"{num}_{title}"
            
            dst = cat_dir / new_name
            if dst != problem_dir:
                print(f"Renaming {name} -> {new_name}")
                if dst.exists():
                    print(f"  Warning: {new_name} already exists. Merging.")
                    # Move files instead
                    for f in problem_dir.iterdir():
                        shutil.move(str(f), str(dst / f.name))
                    shutil.rmtree(problem_dir)
                else:
                    shutil.move(str(problem_dir), str(dst))
        else:
            print(f"Could not parse name: {name}")

print("Refining complete.")
