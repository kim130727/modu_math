from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "examples" / "problems"


def _unit_topic_for(grade: int, semester: int, unit_number: int) -> str:
    if grade == 3 and semester == 1:
        topics = {
            1: "덧셈과 뺄셈",
            2: "평면도형",
            3: "나눗셈",
            4: "곱셈",
            5: "길이와 시간",
            6: "분수와 소수",
        }
        return topics.get(unit_number, "수학")
    if grade == 3 and semester == 2:
        topics = {
            1: "곱셈",
            2: "나눗셈",
            3: "원",
            4: "분수",
            5: "들이와 무게",
            6: "자료의 정리",
        }
        return topics.get(unit_number, "수학")
    return "수학"


def _summary_title(metadata: dict[str, object], unit_topic: str) -> str:
    candidate = metadata.get("question") or metadata.get("title") or metadata.get("instruction")
    if candidate and isinstance(candidate, str) and not re.search(r"\?\?+", candidate):
        return candidate.strip()
    return f"{unit_topic} 문제"


PROBLEM_UNIT_INFO = {
    "008541": (3, 1, 1, "덧셈과 뺄셈", "계산 결과가 큰 것부터 차례대로 나열하기"),
    "008661": (3, 1, 2, "평면도형", "길이가 가장 긴 선분 찾기"),
    "008631": (3, 1, 3, "나눗셈", "수 모형을 보고 알맞은 몫 고르기"),
    "008540": (3, 1, 4, "곱셈", "색칠한 부분에 해당하는 곱셈식 찾기"),
    "008728": (3, 1, 6, "분수와 소수", "그림을 보고 분수를 바르게 말한 사람 찾기"),
    "008732": (3, 1, 6, "분수와 소수", "사다리 결과로 분수 분류 판단하기"),
    "008664": (3, 2, 3, "원", "원을 가장 크게 그릴 수 있는 구멍 고르기"),
    "008713": (3, 2, 3, "원", "반지름이 1 cm인 원을 그리는 순서"),
    "008745": (3, 2, 5, "들이와 무게", "같은 그릇에 옮겨 담아 들이 비교하기"),
    "008751": (3, 2, 5, "들이와 무게", "물병과 우유병의 들이 비교 방법 판단하기"),
}


def _parse_unit_info(renderer_path: Path, file_prefix: str, metadata: dict[str, object]) -> tuple[int, int, int, str, str]:
    suffix = file_prefix[-6:]
    if suffix in PROBLEM_UNIT_INFO:
        grade, semester, unit_number, unit_topic, _ = PROBLEM_UNIT_INFO[suffix]
        sub_unit = ""
        if isinstance(metadata, dict):
            sub_unit = str(metadata.get("subUnit") or metadata.get("subTopic") or metadata.get("topic") or "").strip()
        if not sub_unit or sub_unit == unit_topic:
            sub_unit = "기본 학습"
        return grade, semester, unit_number, unit_topic, sub_unit

    parts = renderer_path.relative_to(ROOT).parts
    grade = 3
    semester = 1
    unit_number = 1
    unit_topic = ""

    for part in parts:
        sem_m = re.match(r"^(\d+)-(\d+)$", part)
        if sem_m:
            grade = int(sem_m.group(1))
            semester = int(sem_m.group(2))
            continue
        unit_m = re.match(r"^(\d+)_(.+)$", part)
        if unit_m:
            unit_number = int(unit_m.group(1))
            unit_topic = unit_m.group(2).replace("_", " ")
            continue

    if not unit_topic:
        p_match = re.match(r"^P(\d)_(\d)_(\d+)", file_prefix)
        if p_match:
            grade = int(p_match.group(1))
            semester = int(p_match.group(2))
            unit_number = int(p_match.group(3))
        else:
            s_match = re.match(r"^S(\d)_.*_(\d)_", file_prefix)
            if s_match:
                grade = int(s_match.group(1))
        unit_topic = _unit_topic_for(grade, semester, unit_number)

    sub_unit = ""
    if isinstance(metadata, dict):
        sub_unit = str(metadata.get("subUnit") or metadata.get("subTopic") or metadata.get("topic") or "").strip()
    if not sub_unit or sub_unit == unit_topic:
        sub_unit = "기본 학습"

    return grade, semester, unit_number, unit_topic, sub_unit


def _domain_for_topic(topic: str) -> str:
    if topic in ("덧셈과 뺄셈", "나눗셈", "곱셈", "분수와 소수", "분수"):
        return "수와 연산"
    if topic in ("평면도형", "원"):
        return "도형"
    if topic in ("길이와 시간", "들이와 무게"):
        return "측정"
    if topic in ("자료의 정리",):
        return "자료와 가능성"
    return "수학 개념"


def generate():
    renderer_files = sorted(
        [
            path for path in (ROOT / "ko").glob("*.renderer.json")
            if path.is_file()
        ],
        key=lambda p: p.name,
    )

    problems: list[dict[str, object]] = []

    for renderer_path in renderer_files:
        file_prefix = renderer_path.name[: -len(".renderer.json")]
        rel_dir = renderer_path.parent.relative_to(ROOT).as_posix()
        if rel_dir == ".":
            rel_dir = ""

        base_path = renderer_path.with_name(file_prefix)
        semantic_path = base_path.with_name(f"{file_prefix}.semantic.json")
        semantic = {}
        if semantic_path.is_file():
            try:
                semantic = json.loads(semantic_path.read_text(encoding="utf-8"))
            except Exception:
                pass

        metadata = semantic.get("metadata") if isinstance(semantic.get("metadata"), dict) else {}
        grade, semester, unit_number, unit_topic, sub_unit = _parse_unit_info(renderer_path, file_prefix, metadata)
        title = _summary_title(metadata, unit_topic)
        problem_type = str(semantic.get("problem_type") or "unknown")
        domain = _domain_for_topic(unit_topic)

        problems.append(
            {
                "id": file_prefix,
                "grade": grade,
                "subject": "math",
                "unit": unit_topic,
                "domain": domain,
                "type": problem_type,
                "title": title,
                "path": f"examples/problems/{rel_dir}".rstrip("/"),
                "filePrefix": file_prefix,
                "semester": f"{semester}학기",
                "unitNumber": unit_number,
                "unitTopic": unit_topic,
                "problemType": problem_type,
                "subUnit": sub_unit,
                "topic": metadata.get("topic", unit_topic),
            }
        )

    manifest_path = ROOT / "manifest.json"
    manifest_data = {
        "version": "1.0.0",
        "total_problems": len(problems),
        "problems": problems,
    }
    manifest_path.write_text(json.dumps(manifest_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {manifest_path} with {len(problems)} problems.")

    dest_paths = [
        REPO / "apps" / "mobile" / "build" / "flutter_assets" / "examples" / "problems" / "manifest.json",
        REPO / "apps" / "mobile" / "build" / "unit_test_assets" / "examples" / "problems" / "manifest.json",
    ]
    for dest in dest_paths:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(manifest_path, dest)
        print(f"Copied manifest to {dest}")


def verify() -> bool:
    manifest_path = ROOT / "manifest.json"
    if not manifest_path.is_file():
        print(f"Error: {manifest_path} not found.")
        return False

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    problems = data.get("problems", [])
    errors = []

    for item in problems:
        prefix = item.get("filePrefix") or item.get("id")
        rel_path = item.get("path", "")
        base_dir = REPO / rel_path if rel_path else ROOT
        renderer_file = base_dir / f"{prefix}.renderer.json"
        semantic_file = base_dir / f"{prefix}.semantic.json"

        if not renderer_file.is_file():
            # Check if any renderer with this prefix exists anywhere in ROOT
            found = list(ROOT.rglob(f"{prefix}.renderer.json"))
            if not found:
                errors.append(f"Missing renderer: {prefix} (expected at {renderer_file})")

        if not semantic_file.is_file():
            found = list(ROOT.rglob(f"{prefix}.semantic.json"))
            if not found:
                errors.append(f"Missing semantic: {prefix} (expected at {semantic_file})")

    if errors:
        print(f"Verification failed with {len(errors)} errors:")
        for err in errors[:20]:
            print(f"  - {err}")
        return False

    print(f"Verification passed: All {len(problems)} problems have valid assets.")
    return True


if __name__ == "__main__":
    import sys
    if "--verify" in sys.argv:
        if not verify():
            sys.exit(1)
    else:
        generate()
        verify()
