import json
import os
import shutil
import re
from pathlib import Path

root = Path(r"C:\projects\modu_math\sample_data\problems\korea_elementary")
temp_dir = root / "_temp_cleanup"

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

for prob_id, meta in metadata_map.items():
    src = temp_dir / prob_id
    if not src.exists():
        # Maybe it was already moved
        continue
    
    grade_dir = root / meta["grade"]
    topic_dir = grade_dir / meta["topic"]
    topic_dir.mkdir(parents=True, exist_ok=True)
    
    # New name
    new_name = f"{prob_id}_{meta['title']}"
    new_name = "".join([c if c.isalnum() or c in " _-" else "_" for c in new_name]).strip()
    dst = topic_dir / new_name
    
    print(f"Moving {prob_id} to {dst.relative_to(root)}")
    
    # Use copy + remove as a safer alternative to move across potential locks
    try:
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        shutil.rmtree(src)
    except Exception as e:
        print(f"  Error moving {prob_id}: {e}")

# Try to cleanup temp_dir at the end
try:
    if temp_dir.exists() and not list(temp_dir.iterdir()):
        shutil.rmtree(temp_dir)
except:
    pass

print("Resume complete.")
