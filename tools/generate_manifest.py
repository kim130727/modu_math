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
    candidate = metadata.get("title") or metadata.get("question") or metadata.get("instruction")
    if candidate and isinstance(candidate, str) and not re.search(r"\?\?+", candidate):
        return candidate.strip()
    topic = metadata.get("topic")
    if topic and isinstance(topic, str):
        return topic.strip()
    return f"{unit_topic} 문제"


PROBLEM_UNIT_INFO = {
    "008541": (3, 1, 1, "덧셈과 뺄셈", "세 자리 수의 덧셈과 뺄셈"),
    "008661": (3, 1, 2, "평면도형", "선분, 반직선, 직선"),
    "008631": (3, 1, 3, "나눗셈", "(두 자리 수)÷(한 자리 수)"),
    "008540": (3, 1, 4, "곱셈", "(두 자리 수)×(한 자리 수)"),
    "008728": (3, 1, 6, "분수와 소수", "분수만큼 알아보기"),
    "008732": (3, 1, 6, "분수와 소수", "분수의 크기 비교"),
    "008664": (3, 2, 3, "원", "원의 중심과 반지름"),
    "008713": (3, 2, 3, "원", "컴퍼스로 원 그리기"),
    "008745": (3, 2, 5, "들이와 무게", "들이 비교하기"),
    "008751": (3, 2, 5, "들이와 무게", "들이 비교하기"),
}


_STORAGE_CACHE: dict[str, tuple[int, int, int, str]] | None = None


def _get_storage_mapping() -> dict[str, tuple[int, int, int, str]]:
    global _STORAGE_CACHE
    if _STORAGE_CACHE is not None:
        return _STORAGE_CACHE
    mapping = {}
    storage_root = REPO / "examples" / "storage" / "ko"
    if storage_root.is_dir():
        for sem_dir in storage_root.iterdir():
            if not sem_dir.is_dir() or sem_dir.name.startswith("."):
                continue
            sem_m = re.match(r"^(\d+)-(\d+)$", sem_dir.name)
            if not sem_m:
                continue
            grade, semester = int(sem_m.group(1)), int(sem_m.group(2))
            for unit_dir in sem_dir.iterdir():
                if not unit_dir.is_dir():
                    continue
                unit_m = re.match(r"^(\d+)_(.+)$", unit_dir.name)
                if not unit_m:
                    continue
                unit_number = int(unit_m.group(1))
                unit_topic = unit_m.group(2).replace("_", " ")
                for f in unit_dir.rglob("*.json"):
                    stem = f.name.split(".")[0]
                    mapping[stem] = (grade, semester, unit_number, unit_topic)
    _STORAGE_CACHE = mapping
    return mapping


def _infer_unit_from_keywords(text: str) -> tuple[int, int, int, str]:
    if any(k in text for k in ["원", "circle", "지름", "반지름", "중심", "컴퍼스"]):
        return (3, 2, 3, "원")
    if any(k in text for k in ["들이", "무게", "capacity", "weight", "생수병", "물병", "리터", "밀리리터"]):
        return (3, 2, 5, "들이와 무게")
    if any(k in text for k in ["분수", "소수", "fraction"]):
        return (3, 1, 6, "분수와 소수")
    if any(k in text for k in ["곱셈", "multiplication"]):
        return (3, 1, 4, "곱셈")
    if any(k in text for k in ["나눗셈", "division"]):
        return (3, 1, 3, "나눗셈")
    if any(k in text for k in ["평면도형", "직각", "선분", "반직선", "직선", "삼각형", "사각형"]):
        return (3, 1, 2, "평면도형")
    return (3, 1, 1, "덧셈과 뺄셈")


def _infer_sub_unit(unit_topic: str, metadata: dict[str, object], semantic: dict[str, object]) -> str:
    sub = ""
    if isinstance(metadata, dict):
        sub = str(metadata.get("subUnit") or metadata.get("subTopic") or metadata.get("topic") or "").strip()
    if sub and sub != unit_topic and sub != "기본 학습":
        return sub

    text = (
        str(metadata.get("title", "")) + " " +
        str(metadata.get("question", "")) + " " +
        str(metadata.get("instruction", "")) + " " +
        str(semantic.get("problem_type", ""))
    )
    if unit_topic == "원":
        if any(k in text for k in ["컴퍼스", "침을 꽂", "벌린 것"]):
            return "컴퍼스로 원 그리기"
        if any(k in text for k in ["규칙", "모양", "크기가 같은 원", "무늬"]):
            return "원으로 여러 가지 모양 그리기"
        if any(k in text for k in ["지름"]):
            return "원의 지름"
        if any(k in text for k in ["중심", "반지름"]):
            return "원의 중심과 반지름"
        return "원의 중심과 반지름"
    elif unit_topic == "덧셈과 뺄셈":
        if "뺄셈" in text:
            return "세 자리 수의 뺄셈"
        return "세 자리 수의 덧셈"
    elif unit_topic == "평면도형":
        return "선분, 반직선, 직선"
    elif unit_topic == "나눗셈":
        return "(두 자리 수)÷(한 자리 수)"
    elif unit_topic == "곱셈":
        return "(두 자리 수)×(한 자리 수)"
    elif unit_topic == "분수와 소수":
        return "분수만큼 알아보기"
    elif unit_topic == "들이와 무게":
        return "들이 비교하기"
    return "기본 학습"


def _parse_unit_info(
    renderer_path: Path,
    file_prefix: str,
    metadata: dict[str, object],
    semantic: dict[str, object] | None = None,
) -> tuple[int, int, int, str, str]:
    suffix = file_prefix[-6:]
    if suffix in PROBLEM_UNIT_INFO:
        grade, semester, unit_number, unit_topic, default_sub_unit = PROBLEM_UNIT_INFO[suffix]
        sub_unit = ""
        if isinstance(metadata, dict):
            sub_unit = str(metadata.get("subUnit") or metadata.get("subTopic") or metadata.get("topic") or "").strip()
        if not sub_unit or sub_unit == unit_topic:
            sub_unit = default_sub_unit or "기본 학습"
        return grade, semester, unit_number, unit_topic, sub_unit

    storage_map = _get_storage_mapping()
    if file_prefix in storage_map:
        grade, semester, unit_number, unit_topic = storage_map[file_prefix]
        sub_unit = _infer_sub_unit(unit_topic, metadata, semantic or {})
        return grade, semester, unit_number, unit_topic, sub_unit

    parts = renderer_path.relative_to(ROOT).parts if renderer_path.is_relative_to(ROOT) else ()
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
            unit_topic = _unit_topic_for(grade, semester, unit_number)
        else:
            text = (
                str(metadata.get("title", "")) + " " +
                str(metadata.get("question", "")) + " " +
                str(metadata.get("instruction", "")) + " " +
                str((semantic or {}).get("problem_type", ""))
            )
            grade, semester, unit_number, unit_topic = _infer_unit_from_keywords(text)

    sub_unit = _infer_sub_unit(unit_topic, metadata, semantic or {})
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
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modu_math_web.settings")
    import django
    django.setup()
    from modu_math_web.editor.services.content_store import list_content, read_content

    problems: list[dict[str, object]] = []

    for paths in list_content(ROOT, language="ko"):
        file_prefix = paths.artifact_base
        bundle = read_content(paths)
        semantic = bundle.get("semantic") or {}
        metadata = semantic.get("metadata") if isinstance(semantic.get("metadata"), dict) else {}
        grade, semester, unit_number, unit_topic, sub_unit = _parse_unit_info(
            paths.artifact_path("renderer"), file_prefix, metadata, semantic
        )
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
                "path": "examples/problems/ko",
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
        REPO / "apps" / "mobile" / "generated" / "examples" / "problems" / "manifest.json",
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

    gen_dir = REPO / "apps" / "mobile" / "generated" / "examples" / "problems" / "ko"

    for item in problems:
        prefix = item.get("filePrefix") or item.get("id")
        rel_path = item.get("path", "")
        base_dir = REPO / rel_path if rel_path else ROOT
        renderer_file = base_dir / f"{prefix}.renderer.json"
        semantic_file = base_dir / f"{prefix}.semantic.json"

        if not renderer_file.is_file() and not (gen_dir / f"{prefix}.renderer.json").is_file():
            found = list(ROOT.rglob(f"{prefix}.renderer.json"))
            if not found:
                errors.append(f"Missing renderer: {prefix} (expected at {renderer_file})")

        if not semantic_file.is_file() and not (gen_dir / f"{prefix}.semantic.json").is_file():
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
