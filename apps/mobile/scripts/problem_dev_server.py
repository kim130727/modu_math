from __future__ import annotations

import argparse
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


DEFAULT_ROOT = Path(__file__).resolve().parents[3] / "examples" / "problems"


class ProblemDevHandler(BaseHTTPRequestHandler):
    root: Path

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
        paths = sorted(
            path.relative_to(self.root).as_posix()
            for path in self.root.rglob("*.renderer.json")
            if path.is_file()
        )
        self._send_json({"root": str(self.root), "paths": paths})

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
    parser.add_argument("--host", default="localhost")
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
