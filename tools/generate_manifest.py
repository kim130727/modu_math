from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "examples" / "problems"


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


def _parse_prefix_numbers(file_prefix: str) -> tuple[int, int, int]:
    p_match = re.match(r"^P(\d)_(\d)_(\d+)", file_prefix)
    if p_match:
        return int(p_match.group(1)), int(p_match.group(2)), int(p_match.group(3))
    s_match = re.match(r"^S(\d)_.*_(\d)_", file_prefix)
    if s_match:
        grade = int(s_match.group(1))
        unit = int(s_match.group(2))
        return grade, 1, unit
    return 3, 1, 1


def generate():
    renderer_files = sorted(
        [path for path in ROOT.rglob("*.renderer.json") if path.is_file()],
        key=lambda p: p.name,
    )

    problems: list[dict[str, object]] = []

    for renderer_path in renderer_files:
        file_prefix = renderer_path.name[: -len(".renderer.json")]
        rel_dir = renderer_path.parent.relative_to(ROOT).as_posix()
        if rel_dir == ".":
            rel_dir = ""

        grade, semester, unit_number = _parse_prefix_numbers(file_prefix)
        unit_topic = _unit_topic_for(grade, semester, unit_number)

        base_path = renderer_path.with_name(file_prefix)
        semantic_path = base_path.with_name(f"{file_prefix}.semantic.json")
        semantic = {}
        if semantic_path.is_file():
            try:
                semantic = json.loads(semantic_path.read_text(encoding="utf-8"))
            except Exception:
                pass

        metadata = semantic.get("metadata") if isinstance(semantic.get("metadata"), dict) else {}
        title = _summary_title(metadata, unit_topic)
        problem_type = str(semantic.get("problem_type") or "unknown")

        problems.append(
            {
                "id": file_prefix,
                "grade": grade,
                "subject": "math",
                "unit": f"{semester}학기 {unit_number}. {unit_topic}",
                "type": problem_type,
                "title": title,
                "path": f"examples/problems/{rel_dir}".rstrip("/"),
                "filePrefix": file_prefix,
                "semester": f"{semester}학기",
                "unitNumber": unit_number,
                "unitTopic": unit_topic,
                "problemType": problem_type,
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


if __name__ == "__main__":
    generate()
