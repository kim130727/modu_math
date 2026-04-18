import json
import os
import shutil
import re
from pathlib import Path

root = Path(r"C:\projects\modu_math\sample_data\problems\ke_3rd")

# Define correct titles for original problems
original_titles = {
    "3rd_addition_subtraction_0001": "기호 수식",
    "3rd_addition_subtraction_0002": "덧셈 식",
    "3rd_addition_subtraction_0003": "세로셈 빈칸 채우기",
    "3rd_addition_subtraction_0004": "부등식",
    "3rd_addition_subtraction_0005": "종이별 개수",
    "3rd_addition_subtraction_0006": "잘못 계산한 사람",
    "3rd_addition_subtraction_0007": "팀별 합계 비교",
    "3rd_addition_subtraction_0008": "가장 큰 뺄셈",
    "3rd_shape2d_0001": "직각 개수 비교",
    "3rd_shape2d_0002": "직각 삼각형 개수",
    "3rd_shape2d_0003": "각 이름 쓰기",
    "3rd_shape2d_0004": "사각형 각 표시",
    "3rd_shape2d_0005": "사각형 둘레 구하기",
    "3rd_shape2d_0006": "직각의 개수",
    "3rd_shape2d_0007": "삼각형 개수",
    "3rd_shape2d_0008": "사각형과 정사각형",
    "3rd_shape2d_0009": "시각과 직각",
    "3rd_shape2d_0010": "사각형 개수",
    "3rd_shape2d_0011": "선이 아닌 이유",
    "3rd_shape2d_0012": "각의 수 비교",
    "3rd_shape2d_0013": "삼각형 찾기"
}

# My new problems
ke_3rd_titles = {
    "ke_3rd_0001": "바둑돌 빼기",
    "ke_3rd_0002": "모양에 알맞은 수 구하기",
    "ke_3rd_0003": "벌레 먹은 셈 (뺄셈)",
    "ke_3rd_0004": "국어와 수학을 모두 좋아하는 학생 수",
    "ke_3rd_0005": "부등식을 만족하는 가장 큰 자연수",
    "ke_3rd_0006": "수 카드로 만든 수의 차",
    "ke_3rd_0007": "계산 결과가 가장 큰 식 만들기",
    "ke_3rd_0008": "가전제품 소비전력 합산",
    "ke_3rd_0009": "도형 복면산 뺄셈",
    "ke_3rd_0010": "선분의 길이 계산하기"
}

all_titles = {**original_titles, **ke_3rd_titles}

# Mapping categories to final names
category_folders = {
    "1. 길이와 시간": ["ke_3rd_0010"],
    "2. 덧셈과 뺄셈": [k for k in all_titles if "addition_subtraction" in k or ("ke_3rd" in k and k != "ke_3rd_0010")],
    "3. 평면도형": [k for k in all_titles if "shape2d" in k]
}

# 1. First, move all problem folders to a temp location to avoid collisions and nested mess
temp_dir = root / "_temp_cleanup"
temp_dir.mkdir(exist_ok=True)

for p_dir in root.rglob("*"):
    if p_dir.is_dir() and p_dir.parent.parent == root: # Problem level folder
        # Read problem_id from semantic.json
        s_files = list(p_dir.glob("*.semantic.json"))
        if s_files:
            with open(s_files[0], "r", encoding="utf-8") as f:
                data = json.load(f)
            prob_id = data.get("problem_id")
            if prob_id:
                # Store in temp with its id
                shutil.move(str(p_dir), str(temp_dir / prob_id))

# Remove the (now empty) category folders
for cat in ["1. 길이와 시간", "2. 덧셈과 뺄셈", "3. 평면도형", "덧셈과_뺄셈", "평면도형", "길이와_시간"]:
    d = root / cat
    if d.exists():
        shutil.rmtree(d)

# 2. Re-create and move to correct structure
for cat_name, prob_ids in category_folders.items():
    cat_dir = root / cat_name
    cat_dir.mkdir(parents=True, exist_ok=True)
    
    for prob_id in prob_ids:
        src = temp_dir / prob_id
        if src.exists():
            # Get correct title
            title = all_titles.get(prob_id, "문제")
            # Extract number
            num_match = re.search(r"(\d{4})", prob_id)
            num = num_match.group(1) if num_match else "0000"
            
            # Update title in JSON
            s_files = list(src.glob("*.semantic.json"))
            if s_files:
                with open(s_files[0], "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["title"] = title
                with open(s_files[0], "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            
            # New folder name
            new_name = f"{num}_{title}"
            # Sanitize
            new_name = "".join([c if c.isalnum() or c in " _-" else "_" for c in new_name]).strip()
            
            dst = cat_dir / new_name
            shutil.move(str(src), str(dst))
            print(f"Moved {prob_id} to {cat_name}/{new_name}")

# Cleanup temp
if temp_dir.exists():
    shutil.rmtree(temp_dir)

print("Restoration and final refinement complete.")
