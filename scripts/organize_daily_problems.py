"""Organize problem files in examples/problems/ko into daily sets of 20 problems.
Curriculum-aligned progression:
3-1 1. 덧셈과 뺄셈
3-1 2. 평면도형
3-1 3. 나눗셈
3-1 4. 곱셈
3-1 6. 분수와 소수
3-2 3. 원
3-2 5. 들이와 무게
"""
from __future__ import annotations

import glob
import json
import os
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "src"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modu_math_web.settings")
try:
    import django
    django.setup()
except Exception:
    pass

from tools.generate_manifest import _parse_unit_info, _summary_title


def sub_unit_order(unit_topic: str, sub_unit: str) -> int:
    orders = {
        "덧셈과 뺄셈": [
            "세 자리 수의 덧셈",
            "세 자리 수의 뺄셈",
            "기본 학습",
        ],
        "평면도형": [
            "선분, 반직선, 직선",
            "직각",
            "직각삼각형",
            "직사각형",
            "정사각형",
            "기본 학습",
        ],
        "나눗셈": [
            "(두 자리 수)÷(한 자리 수)",
            "기본 학습",
        ],
        "곱셈": [
            "(두 자리 수)×(한 자리 수)",
            "(세 자리 수)×(한 자리 수)",
            "기본 학습",
        ],
        "분수와 소수": [
            "분수만큼 알아보기",
            "분수의 크기 비교",
            "소수",
            "소수의 크기 비교",
            "기본 학습",
        ],
        "원": [
            "원의 중심과 반지름",
            "원의 지름",
            "컴퍼스로 원 그리기",
            "원으로 여러 가지 모양 그리기",
            "기본 학습",
        ],
        "들이와 무게": [
            "들이 비교하기",
            "들이의 단위",
            "들이의 덧셈과 뺄셈",
            "무게 비교하기",
            "무게의 단위",
            "무게의 덧셈과 뺄셈",
            "기본 학습",
        ],
    }
    unit_list = orders.get(unit_topic, [])
    for idx, name in enumerate(unit_list):
        if name in sub_unit or sub_unit in name:
            return idx
    return 99


def organize():
    ko_dir = REPO_ROOT / "examples" / "problems" / "ko"
    all_renderers = sorted(glob.glob(str(ko_dir / "**" / "*.renderer.json"), recursive=True))

    problems_map: dict[str, dict[str, object]] = {}

    for r_path_str in all_renderers:
        r_path = Path(r_path_str)
        prefix = r_path.name[: -len(".renderer.json")]
        if prefix in problems_map:
            # We already have one instance of this problem recorded
            continue

        sem_path = r_path.with_name(f"{prefix}.semantic.json")
        sem = {}
        if sem_path.exists():
            try:
                sem = json.loads(sem_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        meta = sem.get("metadata", {}) if isinstance(sem.get("metadata"), dict) else {}
        grade, semester, unit_number, unit_topic, sub_unit = _parse_unit_info(
            r_path, prefix, meta, sem
        )
        title = _summary_title(meta, unit_topic)

        # Collect all related files across ko_dir for this prefix
        all_files: set[Path] = set()
        for f in ko_dir.rglob(f"{prefix}.*"):
            if f.is_file() and f.name.startswith(f"{prefix}."):
                all_files.add(f)

        problems_map[prefix] = {
            "prefix": prefix,
            "grade": grade,
            "semester": semester,
            "unitNumber": unit_number,
            "unitTopic": unit_topic,
            "subUnit": sub_unit,
            "title": title,
            "files": all_files,
        }

    print(f"Total unique problems found: {len(problems_map)}")

    def sort_key(item: dict[str, object]) -> tuple:
        grade = item["grade"]
        sem = item["semester"]
        unit_num = item["unitNumber"]
        unit_topic = str(item["unitTopic"])
        sub_unit = str(item["subUnit"])
        sub_idx = sub_unit_order(unit_topic, sub_unit)
        prefix = str(item["prefix"])
        return (grade, sem, unit_num, sub_idx, prefix)

    sorted_problems = sorted(problems_map.values(), key=sort_key)

    # Divide into groups of 20
    batch_size = 20
    daily_groups: list[list[dict[str, object]]] = []
    for i in range(0, len(sorted_problems), batch_size):
        daily_groups.append(sorted_problems[i : i + batch_size])

    print(f"Divided into {len(daily_groups)} days.")

    # Move files to day_XX
    for day_idx, group in enumerate(daily_groups, start=1):
        day_dir_name = f"day_{day_idx:02d}"
        target_dir = ko_dir / day_dir_name
        target_dir.mkdir(parents=True, exist_ok=True)
        print(f"Processing {day_dir_name}: {len(group)} problems")

        for prob in group:
            prefix = str(prob["prefix"])
            files: set[Path] = prob["files"]
            for f in files:
                if not f.exists():
                    continue
                # If file is already inside target_dir, skip
                if f.parent.resolve() == target_dir.resolve():
                    continue
                dest = target_dir / f.name
                if dest.exists() and dest != f:
                    # Overwrite if destination already exists (e.g. from duplicates)
                    dest.unlink()
                shutil.move(str(f), str(dest))

    # Clean up empty directories in ko_dir (e.g., 3-1, 3-2, __pycache__)
    for sub in ["3-1", "3-2", "__pycache__"]:
        p = ko_dir / sub
        if p.exists() and p.is_dir():
            shutil.rmtree(p, ignore_errors=True)

    # Check for any remaining stray files directly in ko_dir
    stray = [f for f in ko_dir.iterdir() if f.is_file()]
    print(f"Remaining stray files in {ko_dir}: {len(stray)}")

    print("Organization complete!")


if __name__ == "__main__":
    organize()
