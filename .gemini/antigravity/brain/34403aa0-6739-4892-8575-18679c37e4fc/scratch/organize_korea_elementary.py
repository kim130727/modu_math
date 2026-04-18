import json
import os
import shutil
import re
from pathlib import Path

root = Path(r"C:\projects\modu_math\sample_data\problems\korea_elementary")

# Metadata mapping (Based on analysis)
metadata_map = {
    "0001": {"grade": "3학년", "topic": "평면도형", "title": "직각의 개수"},
    "0002": {"grade": "3학년", "topic": "길이와 시간", "title": "길이 재기"},
    "0003": {"grade": "3학년", "topic": "덧셈과 뺄셈", "title": "수 모형 덧셈 1"},
    "0004": {"grade": "3학년", "topic": "덧셈과 뺄셈", "title": "수 모형 덧셈 2"},
    "0005": {"grade": "3학년", "topic": "덧셈과 뺄셈", "title": "합의 크기 비교"},
    "0006": {"grade": "3학년", "topic": "덧셈과 뺄셈", "title": "계산 검토"},
    "0007": {"grade": "3학년", "topic": "길이와 시간", "title": "선분 거리 계산"},
    "0008": {"grade": "3학년", "topic": "덧셈과 뺄셈", "title": "덧셈 암호 해독"},
    "0009": {"grade": "3학년", "topic": "덧셈과 뺄셈", "title": "수직선 덧셈"},
    "0010": {"grade": "3학년", "topic": "덧셈과 뺄셈", "title": "덧셈 기계"},
    "0011": {"grade": "5학년", "topic": "직육면체", "title": "모서리의 합"},
    "0012": {"grade": "5학년", "topic": "직육면체", "title": "전개도 모서리"},
    "0013": {"grade": "6학년", "topic": "자료의 정리", "title": "과일 원그래프"},
    "0014": {"grade": "6학년", "topic": "분수의 나눗셈", "title": "나눗셈 범위"},
    "0015": {"grade": "5학년", "topic": "다각형의 둘레와 넓이", "title": "도형의 둘레"},
    "0016": {"grade": "3학년", "topic": "곱셈", "title": "카드 곱셈"},
    "0017": {"grade": "3학년", "topic": "덧셈과 뺄셈", "title": "도형 수식"},
}

# 1. First, move all problem folders to a temp location and FLATTEN them
temp_dir = root / "_temp_cleanup"
temp_dir.mkdir(exist_ok=True)

for p_dir in root.iterdir():
    if not p_dir.is_dir() or p_dir.name == "_temp_cleanup":
        continue
    
    # Target temp path for this problem
    prob_id = p_dir.name
    prob_temp_dir = temp_dir / prob_id
    prob_temp_dir.mkdir(exist_ok=True)
    
    # Flatten input/output
    for sub in ["input", "output"]:
        sub_dir = p_dir / sub
        if sub_dir.exists() and sub_dir.is_dir():
            for dirpath, dirnames, filenames in os.walk(sub_dir):
                for filename in filenames:
                    src = Path(dirpath) / filename
                    dst = prob_temp_dir / filename
                    if dst.exists():
                        # Conflict handling (usually we want the output version)
                        if "output" in str(src):
                            shutil.copy2(str(src), str(dst))
                    else:
                        shutil.copy2(str(src), str(dst))
    
    # Also move files from the root of p_dir (like .py files)
    for f in p_dir.iterdir():
        if f.is_file():
            shutil.copy2(str(f), str(prob_temp_dir / f.name))

# 2. Cleanup original folders
for p_dir in root.iterdir():
    if p_dir.is_dir() and p_dir.name != "_temp_cleanup":
        shutil.rmtree(p_dir)

# 3. Organize into Grade/Topic structure
for prob_id, meta in metadata_map.items():
    src = temp_dir / prob_id
    if not src.exists():
        continue
    
    grade_dir = root / meta["grade"]
    topic_dir = grade_dir / meta["topic"]
    topic_dir.mkdir(parents=True, exist_ok=True)
    
    # Update title and metadata in semantic.json
    semantic_path = src / f"{prob_id}.semantic.json"
    if semantic_path.exists():
        with open(semantic_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        data["title"] = meta["title"]
        if "metadata" not in data: data["metadata"] = {}
        data["metadata"]["education"] = {
            "level": "elementary",
            "grade": int(meta["grade"][0]),
            "subject": "math",
            "curriculum": "KR"
        }
        data["metadata"]["classification"] = {
            "topic": meta["topic"]
        }
        
        with open(semantic_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # New name: [번호]_[제목]
    new_name = f"{prob_id}_{meta['title']}"
    # Sanitize
    new_name = "".join([c if c.isalnum() or c in " _-" else "_" for c in new_name]).strip()
    
    dst = topic_dir / new_name
    shutil.move(str(src), str(dst))
    print(f"Organized {prob_id} into {meta['grade']}/{meta['topic']}/{new_name}")

# Cleanup temp
if temp_dir.exists():
    shutil.rmtree(temp_dir)

print("korea_elementary organization complete.")
