from __future__ import annotations

import argparse
import json
import mimetypes
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


DEFAULT_ROOT = Path(__file__).resolve().parents[3] / "examples" / "problems"


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
    # e.g., P3_1_01_00040_15608 or S3_초등_3_008540
    p_match = re.match(r"^P(\d)_(\d)_(\d+)", file_prefix)
    if p_match:
        return int(p_match.group(1)), int(p_match.group(2)), int(p_match.group(3))
    s_match = re.match(r"^S(\d)_.*_(\d)_", file_prefix)
    if s_match:
        grade = int(s_match.group(1))
        unit = int(s_match.group(2))
        return grade, 1, unit
    return 3, 1, 1


class ProblemDevHandler(BaseHTTPRequestHandler):
    root: Path
    _cached_manifest: dict[str, object] | None = None

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/problems":
            self._send_problem_list()
            return
        if parsed.path.startswith("/api/problem-bundle/"):
            self._send_problem_bundle(parsed.path.removeprefix("/api/problem-bundle/"))
            return
        if parsed.path.startswith("/files/"):
            self._send_problem_file(parsed.path.removeprefix("/files/"))
            return
        self._send_json(
            {
                "ok": True,
                "endpoints": [
                    "/api/problems",
                    "/api/problem-bundle/<prefix>",
                    "/files/<relative-path>",
                ],
            }
        )

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.end_headers()

    def _send_problem_list(self) -> None:
        if ProblemDevHandler._cached_manifest is not None:
            self._send_json(ProblemDevHandler._cached_manifest)
            return

        renderer_files = sorted(
            [path for path in self.root.rglob("*.renderer.json") if path.is_file()],
            key=lambda p: p.name,
        )

        paths = [path.relative_to(self.root).as_posix() for path in renderer_files]
        problems: list[dict[str, object]] = []

        for renderer_path in renderer_files:
            file_prefix = renderer_path.name[: -len(".renderer.json")]
            rel_dir = renderer_path.parent.relative_to(self.root).as_posix()
            if rel_dir == ".":
                rel_dir = ""

            grade, semester, unit_number = _parse_prefix_numbers(file_prefix)
            unit_topic = _unit_topic_for(grade, semester, unit_number)

            base_path = renderer_path.with_name(file_prefix)
            semantic = self._read_optional_json(base_path.with_name(f"{file_prefix}.semantic.json"))
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

        manifest_payload = {
            "root": str(self.root),
            "paths": paths,
            "problems": problems,
        }
        ProblemDevHandler._cached_manifest = manifest_payload
        self._send_json(manifest_payload)

    def _send_problem_bundle(self, encoded_prefix: str) -> None:
        prefix = unquote(encoded_prefix).replace("\\", "/").strip("/")
        base_path = self._resolve_problem_base_path(prefix)
        if base_path is None:
            self.send_error(404, f"Problem prefix not found: {prefix}")
            return

        bundle: dict[str, object] = {
            "ok": True,
            "prefix": prefix,
            "semantic": self._read_optional_json(base_path.with_name(f"{base_path.name}.semantic.json")),
            "renderer": self._read_optional_json(base_path.with_name(f"{base_path.name}.renderer.json")),
            "layout": self._read_optional_json(base_path.with_name(f"{base_path.name}.layout.json")),
            "solvable": self._read_solvable_json(base_path),
            "svg": self._read_optional_text(base_path.with_name(f"{base_path.name}.svg")),
        }
        self._send_json(bundle)

    def _resolve_problem_base_path(self, prefix: str) -> Path | None:
        direct = self.root / prefix
        if direct.with_name(f"{direct.name}.renderer.json").is_file():
            return direct

        for candidate_name in (prefix, f"{prefix}_ko", f"{prefix}_uk"):
            matches = list(self.root.rglob(f"{candidate_name}.renderer.json"))
            if matches:
                matched_file = matches[0]
                return matched_file.with_name(matched_file.name[: -len(".renderer.json")])
        return None

    def _read_optional_json(self, file_path: Path) -> dict[str, object]:
        if not file_path.is_file():
            return {}
        try:
            return json.loads(file_path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _read_solvable_json(self, base_path: Path) -> dict[str, object]:
        for candidate in (
            "solvable.json",
            "solvable.v1.3.json",
            "solvable.v1.2.json",
            "solvable.v1.1.json",
            "solvable.v1.json",
        ):
            file_path = base_path.with_name(f"{base_path.name}.{candidate}")
            if file_path.is_file():
                try:
                    return json.loads(file_path.read_text(encoding="utf-8"))
                except Exception:
                    continue
        return {}

    def _read_optional_text(self, file_path: Path) -> str:
        if not file_path.is_file():
            return ""
        try:
            return file_path.read_text(encoding="utf-8")
        except Exception:
            return ""

    def _send_problem_file(self, encoded_path: str) -> None:
        relative_path = unquote(encoded_path).replace("\\", "/")
        file_path = (self.root / relative_path).resolve()
        if not self._is_inside_root(file_path) or not file_path.is_file():
            self.send_error(404, "File not found")
            return

        content_type = mimetypes.guess_type(file_path.name)[0] or "text/plain"
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, payload: dict[str, object]) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _is_inside_root(self, path: Path) -> bool:
        try:
            path.relative_to(self.root)
            return True
        except ValueError:
            return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        raise SystemExit(f"Problem directory does not exist: {root}")

    ProblemDevHandler.root = root
    server = ThreadingHTTPServer((args.host, args.port), ProblemDevHandler)
    print(f"Serving {root} at http://{args.host}:{args.port}")
    print("Problem list: /api/problems")
    print("Problem bundle: /api/problem-bundle/<prefix>")
    server.serve_forever()


if __name__ == "__main__":
    main()
